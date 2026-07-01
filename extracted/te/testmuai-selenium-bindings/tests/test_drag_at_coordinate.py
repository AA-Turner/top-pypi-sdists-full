"""Tests for testmu_selenium._helpers.drag_at_coordinate.

V2-parity sentinel: viewport-centered offsets anchored on /html/body, with
5px step loop and 0.01s pause per step. Ported from the V2 Selenium
canvas-branch drag implementation.

Defensive error: when execute_script returns None for innerWidth/innerHeight
(page mid-navigation, blocking dialog), the helper raises TestmuConfigError
instead of letting a cryptic TypeError propagate from arithmetic on None.
"""
from unittest.mock import MagicMock, patch, call
import pytest

from testmu_selenium._helpers.drag_at_coordinate import (
    drag_at_coordinate,
    _DRAG_STEP_PX,
)
from testmu_selenium._errors import TestmuConfigError


def _make_fluent_chain():
    chain = MagicMock()
    for method in ("move_to_element_with_offset", "click_and_hold",
                   "move_by_offset", "pause", "release"):
        getattr(chain, method).return_value = chain
    return chain


def _make_driver(vw=1000, vh=800):
    """Driver with a fake execute_script returning given viewport dimensions."""
    driver = MagicMock(name="driver")
    html_body = MagicMock(name="html_body_element")
    driver.find_element.return_value = html_body

    def fake_script(script):
        if "innerWidth" in script:
            return vw
        if "innerHeight" in script:
            return vh
        return None

    driver.execute_script.side_effect = fake_script
    return driver, html_body


@patch("testmu_selenium._helpers.drag_at_coordinate.ActionChains")
def test_drag_at_coordinate_anchors_on_html_body(mock_action_chains):
    chain = _make_fluent_chain()
    mock_action_chains.return_value = chain
    driver, html_body = _make_driver(vw=1000, vh=800)

    # start (500, 400) is centered → offset (0, 0).
    # end (600, 500) → offset (100, 100). delta = (100, 100). steps = 20.
    drag_at_coordinate(driver, 500, 400, 600, 500)

    # Anchored on /html/body via XPath find_element.
    from selenium.webdriver.common.by import By
    driver.find_element.assert_called_once_with(By.XPATH, "/html/body")

    # First call: move_to_element_with_offset(html_body, sx, sy)
    first = chain.method_calls[0]
    assert first[0] == "move_to_element_with_offset"
    assert first.args[0] is html_body
    assert first.args[1] == pytest.approx(0.0)  # 500 - 1000/2
    assert first.args[2] == pytest.approx(0.0)  # 400 - 800/2


@pytest.mark.parametrize(
    "start_x,start_y,end_x,end_y,vw,vh,expected_sx,expected_sy,expected_steps",
    [
        # Centered start, 100×100 delta → 20 steps of (5, 5).
        (500, 400, 600, 500, 1000, 800, 0.0, 0.0, 20),
        # Top-left start, 100×100 delta.
        (0, 0, 100, 100, 1000, 800, -500.0, -400.0, 20),
        # Asymmetric dx > dy: minor axis carried as an integer remainder step,
        # NOT a sub-pixel float (5/6) that move_by_offset would truncate to 0.
        (0, 0, 30, 5, 1000, 800, -500.0, -400.0, 6),
        # Asymmetric dy > dx.
        (0, 0, 5, 30, 1000, 800, -500.0, -400.0, 6),
        # Smaller-than-step delta.
        (0, 0, 3, 0, 1000, 800, -500.0, -400.0, 1),
    ],
)
@patch("testmu_selenium._helpers.drag_at_coordinate.ActionChains")
def test_drag_at_coordinate_offset_math_and_step_loop(
    mock_action_chains, start_x, start_y, end_x, end_y, vw, vh,
    expected_sx, expected_sy, expected_steps,
):
    chain = _make_fluent_chain()
    mock_action_chains.return_value = chain
    driver, html_body = _make_driver(vw=vw, vh=vh)

    drag_at_coordinate(driver, start_x, start_y, end_x, end_y)

    # Anchor offset.
    first = chain.method_calls[0]
    assert first[0] == "move_to_element_with_offset"
    assert first.args[0] is html_body
    assert first.args[1] == pytest.approx(expected_sx)
    assert first.args[2] == pytest.approx(expected_sy)

    # Step loop: every step is an INTEGER bounded by ±5px, so move_by_offset's
    # int() truncation is a no-op (exact-displacement summing is asserted in
    # test_drag_at_coordinate_steps_sum_to_exact_displacement).
    move_offset_calls = [
        c for c in chain.method_calls if c[0] == "move_by_offset"
    ]
    pause_calls = [c for c in chain.method_calls if c[0] == "pause"]
    assert len(move_offset_calls) == expected_steps
    assert len(pause_calls) == expected_steps
    for c in move_offset_calls:
        step_x, step_y = c.args
        assert isinstance(step_x, int) and isinstance(step_y, int)
        assert abs(step_x) <= _DRAG_STEP_PX and abs(step_y) <= _DRAG_STEP_PX
    for c in pause_calls:
        assert c.args == (0.01,)


@pytest.mark.parametrize(
    "start_x,start_y,end_x,end_y",
    [
        # Dominant-axis undershoot: naive 71*int(352/71)=71*int(4.957)=284 vs 352.
        (0, 0, 352, 239),
        # Minor-axis COLLAPSE: naive dy step 5/6=0.833 -> int() -> 0 -> dy=0 vs 5.
        (0, 0, 30, 5),
        # Negative dominant + minor-axis collapse: delta (-47, -8).
        (100, 200, 53, 192),
    ],
)
@patch("testmu_selenium._helpers.drag_at_coordinate.ActionChains")
def test_drag_at_coordinate_steps_sum_to_exact_displacement(
    mock_action_chains, start_x, start_y, end_x, end_y,
):
    """The drag must travel the FULL requested displacement, pixel-exact.

    Selenium's PointerActions.move_by truncates each axis via int(x), int(y)
    (toward zero), so the true on-screen displacement is the sum of the
    int-truncated per-step deltas — NOT the floats we hand to move_by_offset.
    Naive float steps (delta/steps) drop every per-step fraction and the drag
    undershoots; when a minor axis' per-step delta is < 1px it truncates to 0
    and that axis collapses entirely. The integer +/-5 step + remainder loop
    must sum to the exact delta on both axes.
    """
    chain = _make_fluent_chain()
    mock_action_chains.return_value = chain
    driver, _ = _make_driver(vw=1000, vh=800)

    drag_at_coordinate(driver, start_x, start_y, end_x, end_y)

    move_calls = [c for c in chain.method_calls if c[0] == "move_by_offset"]
    # Mirror Selenium's int() truncation of each step before summing.
    travelled_x = sum(int(c.args[0]) for c in move_calls)
    travelled_y = sum(int(c.args[1]) for c in move_calls)
    assert (travelled_x, travelled_y) == (end_x - start_x, end_y - start_y)


@patch("testmu_selenium._helpers.drag_at_coordinate.ActionChains")
def test_drag_at_coordinate_raises_when_inner_width_unavailable(mock_action_chains):
    """Defensive error on execute_script returning None for innerWidth."""
    chain = _make_fluent_chain()
    mock_action_chains.return_value = chain
    driver = MagicMock()
    driver.find_element.return_value = MagicMock()
    driver.execute_script.return_value = None  # both width and height return None

    with pytest.raises(TestmuConfigError) as excinfo:
        drag_at_coordinate(driver, 100, 100, 200, 200)

    assert "viewport" in str(excinfo.value).lower()


def test_drag_at_coordinate_does_not_call_run_action(monkeypatch):
    """Helper must NOT invoke _run_action — no element to heal."""
    from testmu_selenium import _action_engine
    sentinel = []

    def fake_run_action(*args, **kwargs):
        sentinel.append((args, kwargs))

    monkeypatch.setattr(_action_engine, "_run_action", fake_run_action)

    driver, _ = _make_driver()
    with patch("testmu_selenium._helpers.drag_at_coordinate.ActionChains"):
        drag_at_coordinate(driver, 0, 0, 10, 10)

    assert sentinel == []


def test_drag_at_coordinate_is_publicly_exported():
    import testmu_selenium
    assert hasattr(testmu_selenium, "drag_at_coordinate")
    assert "drag_at_coordinate" in testmu_selenium.__all__
