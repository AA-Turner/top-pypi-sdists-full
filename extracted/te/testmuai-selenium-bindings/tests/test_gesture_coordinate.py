"""Tests for coordinate-tier gestures (ActionBuilder pointer_action; no modifiers)."""
from unittest.mock import MagicMock, patch

from testmu_selenium._helpers import gesture
from testmu_selenium._helpers.gesture import do_gesture_at_coordinate


class CapturingAB:
    instances = []

    def __init__(self, _driver):
        self.pointer_action = MagicMock(name="pointer_action")
        self.key_action = MagicMock(name="key_action")
        self.perform = MagicMock(name="perform")
        CapturingAB.instances.append(self)


def _patch_ab():
    CapturingAB.instances = []
    return patch.object(gesture, "ActionBuilder", side_effect=CapturingAB)


def test_coord_long_press_holds_with_buffer():
    driver = MagicMock(name="driver")
    with _patch_ab():
        assert do_gesture_at_coordinate(
            driver, 120, 240, {"kind": "long_press", "duration": 2.0}
        ) is True
    ab = CapturingAB.instances[0]
    ab.pointer_action.move_to_location.assert_called_once_with(120, 240)
    ab.pointer_action.click_and_hold.assert_called_once()
    ab.pointer_action.pause.assert_called_once_with(2.1)   # 2.0 + 0.1
    ab.pointer_action.release.assert_called_once()
    ab.perform.assert_called_once()


def test_coord_multi_click_two_double_clicks():
    driver = MagicMock(name="driver")
    with _patch_ab():
        do_gesture_at_coordinate(driver, 120, 240, {"kind": "multi_click", "frequency": 2})
    ab = CapturingAB.instances[0]
    ab.pointer_action.move_to_location.assert_called_once_with(120, 240)
    ab.pointer_action.double_click.assert_called_once()
    ab.perform.assert_called_once()


def test_coord_multi_click_five_loops_with_gap():
    driver = MagicMock(name="driver")
    with _patch_ab():
        do_gesture_at_coordinate(driver, 120, 240, {"kind": "multi_click", "frequency": 5})
    ab = CapturingAB.instances[0]
    assert ab.pointer_action.click.call_count == 5
    assert ab.pointer_action.pause.call_count == 4          # between, not after last
    ab.pointer_action.pause.assert_called_with(0.1)
    ab.pointer_action.double_click.assert_not_called()
    ab.perform.assert_called_once()


def test_coord_right_click_context_clicks_no_modifiers():
    driver = MagicMock(name="driver")
    with _patch_ab():
        do_gesture_at_coordinate(driver, 120, 240, {"kind": "right_click"})
    ab = CapturingAB.instances[0]
    ab.pointer_action.move_to_location.assert_called_once_with(120, 240)
    ab.pointer_action.context_click.assert_called_once()
    ab.key_action.key_down.assert_not_called()             # coord path never holds keys
    ab.perform.assert_called_once()
