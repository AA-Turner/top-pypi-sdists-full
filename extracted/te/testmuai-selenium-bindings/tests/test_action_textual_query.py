"""Tests for testmu_selenium.textual_query — high-level healed textual-query verb.

Strategy mirrors test_action_click.py:
- patch _run_action at the wrapper-module path for kwarg-threading tests.
- patch findElement / _heal_cascade / time.sleep at the engine-module path for
  integration tests that exercise the full find→heal→extract loop.

(a) first-try success: findElement returns element, extract returns value.
(b) HEAL path: findElement raises NoSuchElementException, _heal_cascade returns
    new selector, retry succeeds, verb returns extracted value.
(c) COORDINATE heal: _heal_cascade returns coordinates, coord_runner calls
    resolve_coordinate_read, passes element to _extract_value.
(d) regression: raw textualQuery still returns the same value after the refactor.
(e) Selector-less path: _direct_textual_read is the ONLY path (no locate fallback).
"""
from unittest.mock import MagicMock, patch, call

import pytest
from selenium.common.exceptions import NoSuchElementException

from testmu_selenium import _action_textual_query as atq
from testmu_selenium._action_textual_query import (
    textual_query,
    _TEXTUAL_QUERY_SPEC,
    _DIRECT_READ_ATTEMPTS,
    _textual_query_runner,
    _textual_query_coord_runner,
)
from testmu_selenium._action_engine import _DEFAULT_RECOVERABLE
from testmu_selenium._heal_cascade import HealResult
from testmu_selenium._helpers._coordinate_resolver import ResolvedTarget


PRIMARY = [{"selector": "#price", "isXPath": False}]
HEALED = [{"selector": "//span[@id='price']", "isXPath": True, "score": 60}]


def _make_element(tag_name="span", text="42.00", outer_html="<span>42.00</span>"):
    el = MagicMock(name="element")
    el.tag_name = tag_name
    el.text = text
    el.get_attribute.side_effect = lambda key: {"outerHTML": outer_html}.get(key)
    el.get_property.return_value = text
    el.is_selected.return_value = False
    el.is_enabled.return_value = True
    el.is_displayed.return_value = True
    el.value_of_css_property.return_value = ""
    el.size = {"width": 0, "height": 0}
    el.aria_role = ""
    return el


# ---------------------------------------------------------------------------
# Spec structure
# ---------------------------------------------------------------------------

def test_textual_query_spec_uses_default_recoverable():
    assert _TEXTUAL_QUERY_SPEC.recoverable_exceptions is _DEFAULT_RECOVERABLE


def test_textual_query_spec_has_coord_runner():
    assert _TEXTUAL_QUERY_SPEC.coord_runner is _textual_query_coord_runner


# ---------------------------------------------------------------------------
# Kwarg threading — patch _run_action at wrapper-module path
# ---------------------------------------------------------------------------

def test_textual_query_calls_run_action_with_spec():
    driver = MagicMock(name="driver")
    with patch.object(atq, "_run_action", return_value="val") as m_run:
        result = textual_query(driver, PRIMARY, selected_attribute_name="text")

    assert result == "val"
    m_run.assert_called_once()
    args, _kw = m_run.call_args
    assert args[0] is driver
    assert args[1] is _TEXTUAL_QUERY_SPEC
    assert args[2] is PRIMARY


def test_textual_query_threads_selected_attribute_name():
    driver = MagicMock(name="driver")
    with patch.object(atq, "_run_action", return_value="x") as m_run:
        textual_query(driver, PRIMARY, selected_attribute_name="href")

    kw = m_run.call_args.kwargs
    assert kw["selected_attribute_name"] == "href"


def test_textual_query_threads_regex_pattern_and_return_type():
    driver = MagicMock(name="driver")
    with patch.object(atq, "_run_action", return_value=42.0) as m_run:
        textual_query(driver, PRIMARY, selected_attribute_name="text",
                      regex_pattern=r"\d+", return_type="number")

    kw = m_run.call_args.kwargs
    assert kw["regex_pattern"] == r"\d+"
    assert kw["return_type"] == "number"


def test_textual_query_threads_autoheal_false():
    driver = MagicMock(name="driver")
    with patch.object(atq, "_run_action", return_value="") as m_run:
        textual_query(driver, PRIMARY, selected_attribute_name="text", autoheal=False)

    kw = m_run.call_args.kwargs
    assert kw["autoheal"] is False


def test_textual_query_threads_tiers():
    driver = MagicMock(name="driver")
    with patch.object(atq, "_run_action", return_value="") as m_run:
        textual_query(driver, PRIMARY, selected_attribute_name="text", tiers=["LIST_XPATHS"])

    kw = m_run.call_args.kwargs
    assert kw["tiers"] == ["LIST_XPATHS"]


# ---------------------------------------------------------------------------
# (a) First-try success — actual extraction runs end-to-end
# ---------------------------------------------------------------------------

def test_first_try_success_returns_extracted_value():
    """findElement returns element immediately; extract_value returns the text."""
    driver = MagicMock(name="driver")
    el = _make_element(tag_name="span", text="hello")

    with patch("testmu_selenium._action_engine.findElement", return_value=el) as m_find, \
         patch("testmu_selenium._action_engine._heal_cascade") as m_heal:
        result = textual_query(
            driver, PRIMARY,
            selected_attribute_name="text",
            description="price label",
        )

    assert result == "hello"
    m_find.assert_called_once()
    m_heal.assert_not_called()


def test_first_try_success_with_return_type_number():
    """Extracts text and coerces to float when return_type='number'."""
    driver = MagicMock(name="driver")
    el = _make_element(tag_name="span", text="42.50")

    with patch("testmu_selenium._action_engine.findElement", return_value=el):
        result = textual_query(
            driver, PRIMARY,
            selected_attribute_name="text",
            return_type="number",
        )

    assert result == 42.50


def test_first_try_success_with_regex_pattern():
    """findElement returns element; regex applied over outerHTML."""
    driver = MagicMock(name="driver")
    el = _make_element(
        tag_name="span",
        text="Total: $99",
        outer_html="<span>Total: $99</span>",
    )

    with patch("testmu_selenium._action_engine.findElement", return_value=el):
        result = textual_query(
            driver, PRIMARY,
            selected_attribute_name="text",
            regex_pattern=r"\$(\d+)",
        )

    assert result == "99"


# ---------------------------------------------------------------------------
# (b) HEAL path — first findElement raises, cascade returns new selector,
#     retry succeeds and verb returns the extracted value.
# ---------------------------------------------------------------------------

def test_heal_path_retries_with_new_selector():
    """NoSuchElementException on first try → _heal_cascade → healed selector → success."""
    driver = MagicMock(name="driver")
    el2 = _make_element(tag_name="p", text="discounted")

    heal_result = HealResult(
        selectors=HEALED,
        frame_info=None,
        selector_payload=None,
        tier_used="LIST_XPATHS",
        latency_ms=5,
    )

    with patch("testmu_selenium._action_engine.findElement",
               side_effect=[NoSuchElementException("miss"), el2]) as m_find, \
         patch("testmu_selenium._action_engine._heal_cascade",
               return_value=heal_result) as m_heal, \
         patch("testmu_selenium._action_engine.time.sleep"):
        result = textual_query(
            driver, PRIMARY,
            selected_attribute_name="text",
            retry_delay=0,
        )

    assert result == "discounted"
    assert m_find.call_count == 2
    m_heal.assert_called_once()


def test_heal_path_second_findelement_uses_healed_selector():
    """Engine must rebind to heal_result.selectors on the retry findElement call."""
    driver = MagicMock(name="driver")
    el2 = _make_element(tag_name="p", text="ok")

    heal_result = HealResult(
        selectors=HEALED,
        frame_info=None,
        selector_payload=None,
        tier_used="LIST_XPATHS",
        latency_ms=3,
    )

    with patch("testmu_selenium._action_engine.findElement",
               side_effect=[NoSuchElementException("miss"), el2]) as m_find, \
         patch("testmu_selenium._action_engine._heal_cascade",
               return_value=heal_result), \
         patch("testmu_selenium._action_engine.time.sleep"):
        textual_query(driver, PRIMARY, selected_attribute_name="text", retry_delay=0)

    second_call_selector = m_find.call_args_list[1].args[1]
    assert second_call_selector == HEALED


# ---------------------------------------------------------------------------
# (c) COORDINATE heal — coord_runner path
# ---------------------------------------------------------------------------

def test_textual_query_coord_runner_uses_read_resolver_then_findelement():
    """Unit test: _textual_query_coord_runner calls resolve_coordinate_read then findElement."""
    driver = MagicMock(name="driver")
    el = _make_element(tag_name="div", text="at-coords")
    resolved = ResolvedTarget(xpath="//div[1]", meta={"tag": "div", "id": "", "text": ""})
    with patch.object(atq, "resolve_coordinate_read", return_value=resolved) as m_res, \
         patch.object(atq, "findElement", return_value=el) as m_find:
        result = atq._textual_query_coord_runner(driver, 200, 300, {
            "driver": driver, "frame_info": None,
            "selected_attribute_name": "text", "regex_pattern": None, "return_type": None})
    assert result == "at-coords"
    m_res.assert_called_once_with(driver, 200, 300)
    m_find.assert_called_once()                  # read via WebElement, not raw handle


def test_textual_query_coord_runner_raises_when_resolver_returns_none():
    """When resolve_coordinate_read returns None, coord_runner raises NoSuchElementException."""
    driver = MagicMock(name="driver")
    with patch.object(atq, "resolve_coordinate_read", return_value=None):
        with pytest.raises(NoSuchElementException):
            atq._textual_query_coord_runner(driver, 100, 50, {
                "driver": driver, "frame_info": None,
                "selected_attribute_name": "text", "regex_pattern": None, "return_type": None})


def test_selector_present_xpath_preferred_coord_fallback_preserved():
    """Frozen contract for the selector-PRESENT path after Edit 2 read-tunes the coord_runner.

    What is preserved:
      (i)  Selector preferred over coordinates: findElement succeeds → resolve_coordinate_read
           is never called.
      (ii) Coord-fallback returns a local read: findElement misses, cascade returns coords,
           coord_runner derives an xpath and reads locally → result returned.

    Contract change (intentional, documented): when the read-resolver returns None
    (iframe/canvas/closed-shadow/verify-fail — sub-case iii), the selector-present coord
    fallback now raises NoSuchElementException rather than returning a best-effort value
    from a raw elementFromPoint handle. This is an honest hard-fail: the selector-present
    path is NOT wrapped in the selector-less try/except, so the caller knows which element
    it was trying to read and can act accordingly. _direct_textual_read is NOT called
    (the server-snapshot fallback applies only to the selector-LESS branch).
    """
    driver = MagicMock(name="driver")
    el = _make_element(tag_name="span", text="xpath-wins")

    # (i) xpath-preferred: findElement succeeds immediately → resolve_coordinate_read unused
    with patch("testmu_selenium._action_engine.findElement", return_value=el), \
         patch.object(atq, "resolve_coordinate_read") as m_rcr:
        result = textual_query(driver, PRIMARY, selected_attribute_name="text")
    assert result == "xpath-wins"
    m_rcr.assert_not_called()

    # (ii) coord fallback: findElement raises, heal returns coords, resolver returns xpath
    el2 = _make_element(tag_name="div", text="coord-fallback")
    resolved = ResolvedTarget(xpath="//div[1]", meta={"tag": "div", "id": "", "text": ""})
    heal_result = HealResult(selectors=[], coordinates=(100, 200),
                             tier_used="DESKTOP_LOCATE", latency_ms=3)
    with patch("testmu_selenium._action_engine.findElement",
               side_effect=NoSuchElementException("miss")), \
         patch("testmu_selenium._action_engine._heal_cascade", return_value=heal_result), \
         patch("testmu_selenium._action_engine.time.sleep"), \
         patch.object(atq, "resolve_coordinate_read", return_value=resolved), \
         patch.object(atq, "findElement", return_value=el2):
        result2 = textual_query(driver, PRIMARY, selected_attribute_name="text")
    assert result2 == "coord-fallback"

    # (iii) coord fallback, resolver returns None (iframe/canvas/closed-shadow/verify-fail):
    # coord_runner raises NoSuchElementException; _direct_textual_read is NOT called
    # (the server-fallback wrapping applies only to the selector-less branch).
    heal_result_coords_only = HealResult(selectors=[], coordinates=(200, 300),
                                         tier_used="DESKTOP_LOCATE", latency_ms=2)
    with patch("testmu_selenium._action_engine.findElement",
               side_effect=NoSuchElementException("miss")), \
         patch("testmu_selenium._action_engine._heal_cascade",
               return_value=heal_result_coords_only), \
         patch("testmu_selenium._action_engine.time.sleep"), \
         patch.object(atq, "resolve_coordinate_read", return_value=None), \
         patch.object(atq, "_direct_textual_read") as m_direct:
        with pytest.raises(NoSuchElementException):
            textual_query(driver, PRIMARY, selected_attribute_name="background_color")
    m_direct.assert_not_called()


# ---------------------------------------------------------------------------
# Runner unit tests — _textual_query_runner
# ---------------------------------------------------------------------------

def test_textual_query_runner_calls_extract_value_and_returns_result():
    """_textual_query_runner passes element and ctx fields to _extract_value."""
    driver = MagicMock(name="driver")
    el = _make_element(tag_name="span", text="runner-val")

    ctx = {
        "driver": driver,
        "frame_info": None,
        "selected_attribute_name": "text",
        "regex_pattern": None,
        "return_type": None,
    }
    result = _textual_query_runner(el, ctx)
    assert result == "runner-val"


# ---------------------------------------------------------------------------
# (e) Selector-less path — _direct_textual_read is the ONLY path.
#     The DESKTOP_LOCATE_FULL_PAGE_READ locate tier was REMOVED because
#     /v2/locate/desktop refuses read/inspect intents by protocol, so it
#     never resolved a textual_query. Selector-less now goes straight to
#     _direct_textual_read with no fallback.
# ---------------------------------------------------------------------------

def _resp(text):
    r = MagicMock(name="response")
    r.text = text
    return r


def test_empty_selector_calls_direct_read_only():
    """textual_query(driver, [], ...) calls _direct_textual_read and NEVER _run_action.

    The locate fallback no longer exists — /v2/locate/desktop rejects read intents
    by protocol, so the only path is the direct server snapshot read.
    """
    driver = MagicMock(name="driver")
    with patch.object(atq, "_direct_textual_read", return_value="server-val") as m_direct, \
         patch.object(atq, "_run_action") as m_run:
        result = textual_query(driver, [], selected_attribute_name="text",
                               description="the label")
    assert result == "server-val"
    m_direct.assert_called_once()
    m_run.assert_not_called()


# ---------------------------------------------------------------------------
# Direct-read unit tests
# ---------------------------------------------------------------------------

def test_direct_read_builds_endpoint_required_current_action():
    """current_action must carry the fields /v1/heal/textual_query hard-subscripts:
    operation_id, instruction_id, and sub_instruction_obj.operation_dict.
    Missing any of these 500s the endpoint."""
    driver = MagicMock(name="driver")
    captured = {}

    class _FakeHeal:
        def __init__(self, current_action, drv, **kw):
            captured["current_action"] = current_action

        def textual_query_v2(self, a11y, dom, vp):
            return _resp('{"value": "ok"}')

    with patch.object(atq, "capture_a11y_dom_snapshot", return_value=({}, {}, None)), \
         patch.object(atq, "Heal", _FakeHeal), \
         patch.object(atq, "SmartWait"), \
         patch("testmu_selenium._action_textual_query.time.sleep"):
        atq._direct_textual_read(driver, selected_attribute_name="value",
                                 return_type=None, description="Read input field value")

    ca = captured["current_action"]
    assert "operation_id" in ca
    assert "instruction_id" in ca
    op_dict = ca["sub_instruction_obj"]["operation_dict"]
    assert op_dict["queried_value"] == "Read input field value"
    # top-level selected_attribute must NOT be present (would UnboundLocalError
    # result_type server-side); the attribute rides inside operation_dict.
    assert "selected_attribute" not in ca


def test_direct_read_coerces_number_return_type():
    driver = MagicMock(name="driver")

    with patch.object(atq, "capture_a11y_dom_snapshot", return_value=({}, {}, None)), \
         patch.object(atq, "Heal") as m_heal_cls, \
         patch.object(atq, "SmartWait"), \
         patch("testmu_selenium._action_textual_query.time.sleep"):
        m_heal_cls.return_value.textual_query_v2.return_value = _resp('{"value": "42.50"}')
        result = atq._direct_textual_read(driver, selected_attribute_name="value",
                                          return_type="number", description="x")

    assert result == 42.50


def test_direct_read_raises_on_endpoint_error():
    """Error payload on every attempt → loop exhausts all _DIRECT_READ_ATTEMPTS retries
    and raises NoSuchElementException. textual_query_v2 is called exactly _DIRECT_READ_ATTEMPTS
    times (one per attempt)."""
    driver = MagicMock(name="driver")

    with patch.object(atq, "capture_a11y_dom_snapshot", return_value=({}, {}, None)), \
         patch.object(atq, "Heal") as m_heal_cls, \
         patch.object(atq, "SmartWait"), \
         patch("testmu_selenium._action_textual_query.time.sleep"):
        m_heal_cls.return_value.textual_query_v2.return_value = _resp('{"error": "boom"}')
        with pytest.raises(NoSuchElementException):
            atq._direct_textual_read(driver, selected_attribute_name="value",
                                     return_type=None, description="x")

    assert m_heal_cls.return_value.textual_query_v2.call_count == _DIRECT_READ_ATTEMPTS


def test_direct_read_calls_smart_wait_before_snapshot():
    """SmartWait.smart_wait() is called, then time.sleep(), then capture_a11y_dom_snapshot.

    An unsettled page (in-flight anchor scroll or late reflow) mislands the
    viewport rect, causing the server to drop the target node and return
    found=false → HTTP 500. Settling must precede snapshotting.
    """
    driver = MagicMock(name="driver")
    call_order: list = []

    sw_instance = MagicMock()
    sw_instance.smart_wait.side_effect = lambda: call_order.append("wait")
    sw_cls = MagicMock(return_value=sw_instance)

    def _fake_sleep(_secs):
        call_order.append("sleep")

    def _fake_capture(drv):
        call_order.append("capture")
        return ({}, {}, None)

    with patch.object(atq, "SmartWait", sw_cls), \
         patch.object(atq, "capture_a11y_dom_snapshot", side_effect=_fake_capture), \
         patch("testmu_selenium._action_textual_query.time.sleep", side_effect=_fake_sleep), \
         patch.object(atq, "Heal") as m_heal_cls:
        m_heal_cls.return_value.textual_query_v2.return_value = _resp('{"value": "ok"}')
        atq._direct_textual_read(driver, selected_attribute_name="text",
                                 return_type=None, description="x")

    # First attempt must settle (wait → sleep) before snapshotting (capture).
    assert call_order[:3] == ["wait", "sleep", "capture"]


# ---------------------------------------------------------------------------
# Retry behaviour of _direct_textual_read
# ---------------------------------------------------------------------------

def test_direct_read_retries_until_success():
    """Error on first two attempts, success on the third: value is returned and
    textual_query_v2 is called exactly 3 times (retry works)."""
    driver = MagicMock(name="driver")

    with patch.object(atq, "capture_a11y_dom_snapshot", return_value=({}, {}, None)), \
         patch.object(atq, "Heal") as m_heal_cls, \
         patch.object(atq, "SmartWait"), \
         patch("testmu_selenium._action_textual_query.time.sleep"):
        m_heal_cls.return_value.textual_query_v2.side_effect = [
            _resp('{"error": "not found"}'),
            _resp('{"error": "timeout"}'),
            _resp('{"value": "final"}'),
        ]
        result = atq._direct_textual_read(driver, selected_attribute_name="text",
                                          return_type=None, description="retry label")

    assert result == "final"
    assert m_heal_cls.return_value.textual_query_v2.call_count == 3


def test_direct_read_raises_after_max_attempts():
    """Error payload on every attempt → raises NoSuchElementException after exactly
    _DIRECT_READ_ATTEMPTS calls. The error message includes the attempt count."""
    driver = MagicMock(name="driver")

    with patch.object(atq, "capture_a11y_dom_snapshot", return_value=({}, {}, None)), \
         patch.object(atq, "Heal") as m_heal_cls, \
         patch.object(atq, "SmartWait"), \
         patch("testmu_selenium._action_textual_query.time.sleep"):
        m_heal_cls.return_value.textual_query_v2.return_value = _resp('{"error": "server down"}')
        with pytest.raises(NoSuchElementException, match=str(_DIRECT_READ_ATTEMPTS)):
            atq._direct_textual_read(driver, selected_attribute_name="text",
                                     return_type=None, description="x")

    assert m_heal_cls.return_value.textual_query_v2.call_count == _DIRECT_READ_ATTEMPTS


# ---------------------------------------------------------------------------
# (d) Regression — raw textualQuery unchanged after refactor
# ---------------------------------------------------------------------------

def test_raw_textual_query_still_works_after_refactor():
    """textualQuery (camelCase, raw) must still return the same value after
    _extract_value refactoring — the extraction path is now shared."""
    from testmu_selenium._helpers.textual_query import textualQuery

    driver = MagicMock(name="driver")
    el = _make_element(tag_name="span", text="legacy-value")
    selector = [{"selector": "#price", "isXPath": False}]

    with patch("testmu_selenium._helpers.textual_query.findElement", return_value=el):
        result = textualQuery(
            driver,
            selector=selector,
            selected_attribute_name="text",
        )

    assert result == "legacy-value"


def test_raw_textual_query_regex_unchanged_after_refactor():
    """Regex path via textualQuery is unchanged after the refactor."""
    from testmu_selenium._helpers.textual_query import textualQuery

    driver = MagicMock(name="driver")
    el = _make_element(
        tag_name="span",
        text="$99",
        outer_html="<span>$99</span>",
    )
    selector = [{"selector": "#price", "isXPath": False}]

    with patch("testmu_selenium._helpers.textual_query.findElement", return_value=el):
        result = textualQuery(
            driver,
            selector=selector,
            selected_attribute_name="text",
            regex_pattern=r"\$(\d+)",
        )

    assert result == "99"
