"""Tests for testmu_selenium.scroll_into_view — high-level scroll_into_view wrapper.

Strategy: stub _run_action at the wrapper-module path so we can assert the
runtime kwargs/spec the wrapper threads through, without exercising the
full engine again (engine itself is covered in test_action_engine.py).
"""
import time
from unittest.mock import MagicMock, patch

import pytest
from selenium.common.exceptions import NoSuchElementException

import testmu_selenium._action_scroll_into_view as asiv
from testmu_selenium._action_scroll_into_view import (
    scroll_into_view, _SCROLL_INTO_VIEW_SPEC, _scroll_into_view_runner,
    _HEAL_TIERS, _SHADOW_HEAL_TIERS, _scroll_coord_runner,
)
from testmu_selenium._action_engine import _DEFAULT_RECOVERABLE
from testmu_selenium._heal_cascade import HealResult


PRIMARY = [{"selector": "#target", "isXPath": False}]


# ---------------------------------------------------------------------------
# Group A — kwarg threading via patched _run_action
# ---------------------------------------------------------------------------

def test_scroll_into_view_calls_run_action_with_spec():
    """scroll_into_view() routes through _run_action, passing _SCROLL_INTO_VIEW_SPEC."""
    driver = MagicMock(name="driver")
    with patch.object(asiv, "_run_action", return_value=None) as m_run:
        result = scroll_into_view(driver, PRIMARY)

    assert result is None
    m_run.assert_called_once()
    args, _kw = m_run.call_args
    assert args[0] is driver
    assert args[1] is _SCROLL_INTO_VIEW_SPEC
    assert args[2] is PRIMARY


def test_scroll_into_view_threads_description_kwarg():
    driver = MagicMock(name="driver")
    with patch.object(asiv, "_run_action", return_value=None) as m_run:
        scroll_into_view(driver, PRIMARY, description="scroll to footer")

    kw = m_run.call_args.kwargs
    assert kw["description"] == "scroll to footer"


def test_scroll_into_view_threads_autoheal_false():
    driver = MagicMock(name="driver")
    with patch.object(asiv, "_run_action", return_value=None) as m_run:
        scroll_into_view(driver, PRIMARY, autoheal=False)

    kw = m_run.call_args.kwargs
    assert kw["autoheal"] is False


def test_scroll_into_view_threads_tiers_kwarg():
    driver = MagicMock(name="driver")
    custom_tiers = ["LIST_XPATHS"]
    with patch.object(asiv, "_run_action", return_value=None) as m_run:
        scroll_into_view(driver, PRIMARY, tiers=custom_tiers)

    kw = m_run.call_args.kwargs
    assert kw["tiers"] == custom_tiers


# ---------------------------------------------------------------------------
# Group B — _scroll_into_view_runner behaviour
# ---------------------------------------------------------------------------

def test_scroll_into_view_runner_calls_execute_script_and_sleeps():
    """Runner calls driver.execute_script with scrollIntoView JS + element,
    then sleeps 1 s (V2-parity settle)."""
    driver = MagicMock(name="driver")
    driver.execute_script = MagicMock()
    element = MagicMock(name="element")

    with patch.object(time, "sleep") as m_sleep:
        result = _scroll_into_view_runner(element, {"driver": driver})

    driver.execute_script.assert_called_once_with(
        "arguments[0].scrollIntoView({block:'center'})", element
    )
    m_sleep.assert_called_once_with(1)
    assert result is None


# ---------------------------------------------------------------------------
# Group C — default recoverable
# ---------------------------------------------------------------------------

def test_scroll_into_view_spec_uses_default_recoverable():
    """_SCROLL_INTO_VIEW_SPEC must inherit the engine's _DEFAULT_RECOVERABLE."""
    assert _SCROLL_INTO_VIEW_SPEC.recoverable_exceptions is _DEFAULT_RECOVERABLE


# ---------------------------------------------------------------------------
# Group D — coord_runner for DESKTOP_LOCATE_FULL_PAGE fallback (spec §9.3)
# ---------------------------------------------------------------------------

def test_scroll_into_view_spec_has_coord_runner():
    """DESKTOP_LOCATE_FULL_PAGE wires a coord_runner: _scroll_coord_runner.
    The tier already centered the target before xpath resolution; the runner is
    an idempotent fine-adjustment via elementFromPoint → scrollIntoView."""
    assert _SCROLL_INTO_VIEW_SPEC.coord_runner is not None
    assert _SCROLL_INTO_VIEW_SPEC.coord_runner is _scroll_coord_runner


# ---------------------------------------------------------------------------
# Extra — coordinate-only HealResult dispatches through _scroll_coord_runner
# ---------------------------------------------------------------------------

def test_coordinate_only_heal_result_dispatches_coord_runner():
    """When heal cascade returns a coordinates-only HealResult (selectors=[]),
    the engine calls _scroll_coord_runner(driver, x, y, ctx) instead of raising
    NotImplementedError. Now that DESKTOP_LOCATE_FULL_PAGE wires a coord_runner,
    this path is valid and should succeed.

    Contrast with test_coordinate_tier_without_coord_runner_raises_typed_error in
    test_action_engine.py, which tests specs that genuinely have no coord_runner."""
    driver = MagicMock(name="driver")
    driver.execute_script = MagicMock(return_value=None)

    heal_result = HealResult(
        selectors=[],
        coordinates=(100, 200),
        tier_used="DESKTOP_LOCATE_FULL_PAGE",
        latency_ms=1,
    )

    with patch("testmu_selenium._action_engine.findElement",
               side_effect=NoSuchElementException("primary miss")), \
         patch("testmu_selenium._action_engine._heal_cascade",
               return_value=heal_result), \
         patch("testmu_selenium._action_engine.time.sleep"):
        # Should NOT raise NotImplementedError — coord_runner is wired
        scroll_into_view(driver, PRIMARY, retry_delay=0)

    # execute_script called by _scroll_coord_runner with the coordinates
    js_calls = [str(c) for c in driver.execute_script.call_args_list]
    assert any("elementFromPoint" in c for c in js_calls), (
        "_scroll_coord_runner must call elementFromPoint"
    )


# ---------------------------------------------------------------------------
# Group E — shadow-aware tier selection (RED until Edit E implemented)
# ---------------------------------------------------------------------------

def test_spec_op_type_is_scroll_until_element():
    """_SCROLL_INTO_VIEW_SPEC.op_type must be 'scroll_until_element' so the heal
    cascade threads the correct operation_type to _heal.py's full-page tagify gate."""
    assert _SCROLL_INTO_VIEW_SPEC.op_type == "scroll_until_element"


def test_shadow_scroll_selects_list_xpaths_first():
    """When search_root is truthy (shadow DOM context), tiers must start with
    LIST_XPATHS so the heal cascade can do full-page tagify and return
    shadow-relative xpaths. VISION_QUERY returns a top-document xpath that can't
    cross a shadow boundary."""
    driver = MagicMock(name="driver")
    search_root = MagicMock(name="shadow_root")
    with patch.object(asiv, "_run_action", return_value=None) as m_run:
        scroll_into_view(driver, PRIMARY, search_root=search_root)

    kw = m_run.call_args.kwargs
    tiers = kw["tiers"]
    assert tiers[0] == "LIST_XPATHS", f"expected LIST_XPATHS first for shadow scroll, got {tiers}"
    assert "VISION_QUERY" in tiers


def test_non_shadow_scroll_uses_desktop_locate_full_page_first():
    """Non-shadow default: ('DESKTOP_LOCATE_FULL_PAGE', 'VISION_QUERY').
    DESKTOP_LOCATE_FULL_PAGE captures a full-page screenshot so the below-fold
    target is visible; VISION_QUERY is the fallback. LIST_XPATHS is suppressed
    (false-positive relocate risk on flat DOM — see V2-parity notes in module)."""
    driver = MagicMock(name="driver")
    with patch.object(asiv, "_run_action", return_value=None) as m_run:
        scroll_into_view(driver, PRIMARY)

    kw = m_run.call_args.kwargs
    assert kw["tiers"] == ('DESKTOP_LOCATE_FULL_PAGE', 'VISION_QUERY'), (
        f"Expected non-shadow tiers=('DESKTOP_LOCATE_FULL_PAGE', 'VISION_QUERY'), got {kw['tiers']}"
    )


def test_scroll_into_view_threads_op_type_to_heal_cascade():
    """_run_action must forward op_type=spec.op_type to _heal_cascade so that
    _synthesize_current_action bakes 'scroll_until_element' into operation_type
    and _heal.py gates full-page tagify correctly.

    With search_root set, the first heal attempt uses LIST_XPATHS. We patch
    findElement to raise NoSuchElementException and _heal_cascade to raise
    AutohealExhausted (so _run_action re-raises), then inspect the captured
    kwargs on the _heal_cascade call."""
    from testmu_selenium._errors import AutohealExhausted
    from testmu_selenium._heal_cascade import HealResult as _HR
    from selenium.common.exceptions import NoSuchElementException as NSE

    driver = MagicMock(name="driver")
    search_root = MagicMock(name="shadow_root")
    captured = {}

    def _fake_heal_cascade(**kw):
        captured.update(kw)
        raise AutohealExhausted(
            original=NSE("miss"),
            last_miss=None,
        )

    with patch("testmu_selenium._action_engine.findElement", side_effect=NSE("primary miss")), \
         patch("testmu_selenium._action_engine._heal_cascade", side_effect=_fake_heal_cascade), \
         patch("testmu_selenium._action_engine.time.sleep"), \
         patch("testmu_selenium._action_engine.SmartWait"):
        with pytest.raises(AutohealExhausted):
            scroll_into_view(driver, PRIMARY, search_root=search_root,
                             max_attempts=2, retry_delay=0)

    assert captured.get("op_type") == "scroll_until_element", (
        f"_heal_cascade must receive op_type='scroll_until_element', got {captured.get('op_type')!r}"
    )


# ---------------------------------------------------------------------------
# Group F — tiers tuple pin (spec §9)
# ---------------------------------------------------------------------------

def test_non_shadow_tiers_constant_is_desktop_locate_full_page_then_vision():
    """_HEAL_TIERS must be ('DESKTOP_LOCATE_FULL_PAGE', 'VISION_QUERY').
    Reverting to ('VISION_QUERY',) would break below-fold scroll healing (V2-parity gap)."""
    assert _HEAL_TIERS == ('DESKTOP_LOCATE_FULL_PAGE', 'VISION_QUERY'), (
        f"Expected _HEAL_TIERS == ('DESKTOP_LOCATE_FULL_PAGE', 'VISION_QUERY'), got {_HEAL_TIERS}"
    )


def test_shadow_tiers_constant_unchanged():
    """Shadow tiers remain ('LIST_XPATHS', 'VISION_QUERY') — shadow path unchanged."""
    assert _SHADOW_HEAL_TIERS == ('LIST_XPATHS', 'VISION_QUERY'), (
        f"Expected _SHADOW_HEAL_TIERS == ('LIST_XPATHS', 'VISION_QUERY'), got {_SHADOW_HEAL_TIERS}"
    )


# ---------------------------------------------------------------------------
# Group G — _scroll_coord_runner (spec §9.3)
# ---------------------------------------------------------------------------

def test_scroll_coord_runner_calls_element_from_point_and_scroll_into_view():
    """_scroll_coord_runner: driver executes elementFromPoint JS, scrollIntoView called."""
    driver = MagicMock(name="driver")
    driver.execute_script = MagicMock(return_value=None)

    result = _scroll_coord_runner(driver, 300, 400, {"driver": driver})

    driver.execute_script.assert_called_once()
    js_call = driver.execute_script.call_args
    # The JS must contain elementFromPoint and scrollIntoView
    js_text = js_call.args[0]
    assert "elementFromPoint" in js_text, "JS must call elementFromPoint"
    assert "scrollIntoView" in js_text, "JS must call scrollIntoView"
    # Coordinates passed as arguments
    assert js_call.args[1] == 300
    assert js_call.args[2] == 400
    assert result is True


def test_scroll_coord_runner_null_safe_when_element_not_found():
    """_scroll_coord_runner: if elementFromPoint returns null, JS no-ops safely (no crash).
    The null-guard 'if (el)' ensures this is safe."""
    driver = MagicMock(name="driver")
    # Simulate JS returning None (null element — target not in viewport)
    driver.execute_script = MagicMock(return_value=None)

    # Must not raise even when the JS would find no element
    result = _scroll_coord_runner(driver, 0, 0, {"driver": driver})
    assert result is True
