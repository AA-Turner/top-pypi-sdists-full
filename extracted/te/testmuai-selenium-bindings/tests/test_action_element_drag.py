"""Tests for testmu_selenium.element_drag wrapper.

V2-parity sentinel: integer 5px step + remainder loop, 0.01s pause per step.

Selenium 4.x's PointerActions.move_by casts both axes via int(x), int(y),
which truncates toward zero. If element_drag passes float step deltas
(dx/steps), each step's actual displacement is smaller than intended; the
cumulative drag undershoots the target. The V2 Selenium drag implementation
avoids this by using a strict integer step of ±5 (or remainder) per
iteration.

Ported from the V2 Selenium drag implementation (non-canvas branch).
"""
from unittest.mock import MagicMock, patch, call
import pytest

from testmu_selenium._action_element_drag import element_drag


def _make_fluent_chain():
    chain = MagicMock()
    for method in ("click_and_hold", "move_by_offset", "pause", "release"):
        getattr(chain, method).return_value = chain
    return chain


@patch("testmu_selenium._action_element_drag.ActionChains")
def test_element_drag_emits_v2_parity_step_loop(mock_action_chains):
    """Even multiple of step size — 4 integer (5, 0) steps."""
    chain = _make_fluent_chain()
    mock_action_chains.return_value = chain

    driver = MagicMock(name="driver")
    el = MagicMock(name="source_element")

    # dx=20, dy=0 → 4 iterations of (5, 0).
    element_drag(driver, el, 20, 0)

    mock_action_chains.assert_called_once_with(driver)
    assert chain.method_calls == [
        call.click_and_hold(el),
        call.move_by_offset(5, 0),
        call.pause(0.01),
        call.move_by_offset(5, 0),
        call.pause(0.01),
        call.move_by_offset(5, 0),
        call.pause(0.01),
        call.move_by_offset(5, 0),
        call.pause(0.01),
        call.release(),
        call.perform(),
    ]


@pytest.mark.parametrize(
    "dx,dy",
    [
        (20, 0),
        (3, 0),
        (-20, -20),
        (5, 5),
        (10, 0),
        # Non-exact divisions — these regress under the float-step bug.
        # With float steps + Selenium's int(x) cast, the cumulative drag
        # under-runs the target. The integer remainder loop reaches it exactly.
        (-352, -239),  # non-exact division: integer remainder loop reaches target exactly
        (-316, -124),  # non-exact division: integer remainder loop reaches target exactly
        (27, 11),      # mixed magnitudes, neither divides evenly by 5
        (1, 1),        # both smaller than step size
        (0, 0),        # degenerate: no drag.
    ],
)
@patch("testmu_selenium._action_element_drag.ActionChains")
def test_element_drag_reaches_target_exactly_with_int_steps(mock_action_chains, dx, dy):
    """Sum of move_by_offset deltas equals (dx, dy); every arg is an int.

    This pins V2-parity and is the RED test for the float-step undershoot:
    Selenium's W3C PointerActions.move_by casts via int(x), int(y) — so a
    float step like -4.957 becomes -4 at the wire, and dx*steps undershoots.
    The fix uses integer ±step_size or remainder.
    """
    chain = _make_fluent_chain()
    mock_action_chains.return_value = chain

    element_drag(MagicMock(), MagicMock(), dx, dy)

    move_offset_calls = [c for c in chain.method_calls if c[0] == "move_by_offset"]
    if dx == 0 and dy == 0:
        assert move_offset_calls == [], "no motion should emit no move_by_offset"
        return

    total_dx = sum(c.args[0] for c in move_offset_calls)
    total_dy = sum(c.args[1] for c in move_offset_calls)
    assert total_dx == dx, f"undershoot on dx: emitted total={total_dx}, expected={dx}"
    assert total_dy == dy, f"undershoot on dy: emitted total={total_dy}, expected={dy}"

    for c in move_offset_calls:
        assert isinstance(c.args[0], int), f"move_by_offset dx must be int, got {type(c.args[0]).__name__}={c.args[0]!r}"
        assert isinstance(c.args[1], int), f"move_by_offset dy must be int, got {type(c.args[1]).__name__}={c.args[1]!r}"

    pause_calls = [c for c in chain.method_calls if c[0] == "pause"]
    assert len(pause_calls) == len(move_offset_calls), "one pause per move_by_offset"
    for c in pause_calls:
        assert c.args == (0.01,)


@patch("testmu_selenium._action_element_drag.ActionChains")
def test_element_drag_no_redundant_move_to_element(mock_action_chains):
    """V2 calls click_and_hold(element) directly — no separate move_to_element.

    click_and_hold(element) already does an implicit move_to_element. Doing it
    twice emits an extra pointerMove on the wire which can confuse page-side
    drag handlers that latch on the first mousemove after mousedown.
    """
    chain = _make_fluent_chain()
    mock_action_chains.return_value = chain

    element_drag(MagicMock(), MagicMock(), 10, 10)

    method_names = [c[0] for c in chain.method_calls]
    assert "move_to_element" not in method_names, (
        f"V2 doesn't call move_to_element; chain methods were: {method_names}"
    )


def test_element_drag_is_publicly_exported():
    import testmu_selenium
    assert hasattr(testmu_selenium, "element_drag")
    assert "element_drag" in testmu_selenium.__all__


# =============================================================================
# Spec §10.2 — selector form routes through _run_action; coordinate runner
# =============================================================================

M = "testmu_selenium._action_element_drag"

SEL = [{"selector": "#slider", "isXPath": False}]


class TestElementDragSelectorForm:
    def test_selector_form_routes_through_run_action(self):
        """Selector list → _run_action with op_type 'click_drag', a coord_runner
        on the spec, and dx/dy threaded as runner kwargs."""
        driver = MagicMock(name="driver")

        with patch(f"{M}._run_action", return_value=True) as m_run:
            element_drag(driver, SEL, 10, 20, description="volume slider",
                         fallback_coordinates=(7, 9))

        m_run.assert_called_once()
        args, kwargs = m_run.call_args
        assert args[0] is driver
        spec = args[1]
        assert spec.op_type == "click_drag"
        assert spec.coord_runner is not None
        assert args[2] == SEL
        assert kwargs["description"] == "volume slider"
        assert kwargs["fallback_coordinates"] == (7, 9)
        assert kwargs["dx"] == 10
        assert kwargs["dy"] == 20

    def test_selector_form_forwards_engine_kwargs(self):
        driver = MagicMock(name="driver")
        root = MagicMock(name="search_root")

        with patch(f"{M}._run_action", return_value=True) as m_run:
            element_drag(driver, SEL, 1, 2, description="d",
                         tiers=["DESKTOP_LOCATE"], autoheal=False,
                         max_attempts=2, retry_delay=0.1, search_root=root)

        kwargs = m_run.call_args.kwargs
        assert kwargs["tiers"] == ["DESKTOP_LOCATE"]
        assert kwargs["autoheal"] is False
        assert kwargs["max_attempts"] == 2
        assert kwargs["retry_delay"] == 0.1
        assert kwargs["search_root"] is root

    def test_webelement_form_never_enters_run_action(self):
        """WebElement form is byte-identical legacy — _run_action untouched."""
        driver = MagicMock(name="driver")
        el = MagicMock(name="source_element")

        with patch(f"{M}._run_action") as m_run, \
             patch(f"{M}.ActionChains"):
            element_drag(driver, el, 10, 10)

        m_run.assert_not_called()

    def test_spec_runner_performs_legacy_gesture(self):
        """The selector-form runner delegates to the legacy element gesture
        with ctx-threaded dx/dy."""
        from testmu_selenium._action_element_drag import _DRAG_SPEC
        chain = _make_fluent_chain()
        driver = MagicMock(name="driver")
        el = MagicMock(name="element")

        with patch(f"{M}.ActionChains", return_value=chain) as m_ac:
            result = _DRAG_SPEC.runner(el, {"driver": driver, "dx": 7, "dy": 0})

        assert result is True
        m_ac.assert_called_once_with(driver)
        assert chain.method_calls == [
            call.click_and_hold(el),
            call.move_by_offset(5, 0),
            call.pause(0.01),
            call.move_by_offset(2, 0),
            call.pause(0.01),
            call.release(),
            call.perform(),
        ]


class TestElementDragCoordRunner:
    def test_coord_runner_drags_by_offset_from_healed_point(self):
        """Healed (x, y) → drag_at_coordinate gesture from (x, y) to
        (x+dx, y+dy)."""
        from testmu_selenium._action_element_drag import _DRAG_SPEC
        driver = MagicMock(name="driver")
        driver.execute_script.return_value = [1280, 720]

        with patch(f"{M}.drag_at_coordinate") as m_drag:
            result = _DRAG_SPEC.coord_runner(driver, 100, 200, {"dx": 50, "dy": -30})

        assert result is True
        m_drag.assert_called_once_with(driver, 100, 200, 150, 170)

    def test_coord_runner_clamps_end_point_to_viewport(self):
        """End point clamps to [0, viewport_dim-1] on both axes."""
        from testmu_selenium._action_element_drag import _DRAG_SPEC
        driver = MagicMock(name="driver")
        driver.execute_script.return_value = [1280, 720]

        with patch(f"{M}.drag_at_coordinate") as m_drag:
            _DRAG_SPEC.coord_runner(driver, 1270, 10, {"dx": 50, "dy": -30})

        m_drag.assert_called_once_with(driver, 1270, 10, 1279, 0)
