"""Coordinate-tier right-click honors held keyboard modifiers (FULL held-keys-coord).

The right_click coord branch holds any keyboard `modifiers` ACROSS the
context_click. Raw ActionBuilder does NOT pad idle device ticks, so a key_up
queued straight after context_click lands on the button-DOWN tick — the modifier
releases before the right-click even fires. The executor drives the keyed
context_click through ActionChains (which pads every tick) so key_up lands AFTER
the pointer-up, mirroring the element-path do_right_click and the Java Actions
coord chain. Held keys ride right_click only (spec §2); long_press/multi_click
coord gestures never receive them. _click_coord_runner threads ctx['modifiers']
into the executor.

These tests inspect the REAL encoded W3C action payload (captured at
driver.execute) rather than mocking ActionBuilder — only a structural assertion
on the per-device tick order can catch the modifier-release-too-early bug.
"""
from unittest.mock import MagicMock

from selenium.webdriver.common.keys import Keys

from testmu_selenium._helpers.gesture import do_gesture_at_coordinate


def _captured_devices(driver):
    """Return {device_type: [tick, ...]} from the last driver.execute W3C payload."""
    enc = driver.execute.call_args[0][1]
    return {dev["type"]: dev["actions"] for dev in enc["actions"]}


def _index_of(ticks, action_type):
    return next(i for i, a in enumerate(ticks) if a["type"] == action_type)


def test_coord_right_click_holds_control_across_context_click():
    driver = MagicMock(name="driver")
    assert do_gesture_at_coordinate(
        driver, 120, 240, {"kind": "right_click"}, ["Control"]
    ) is True
    devices = _captured_devices(driver)
    pointer, key = devices["pointer"], devices["key"]

    # The pointer move anchors at the resolved coords.
    assert any(
        a["type"] == "pointerMove" and a["x"] == 120 and a["y"] == 240
        for a in pointer
    )
    key_down_i = _index_of(key, "keyDown")
    key_up_i = _index_of(key, "keyUp")
    pointer_down_i = _index_of(pointer, "pointerDown")
    pointer_up_i = _index_of(pointer, "pointerUp")
    # Modifier pressed BEFORE the right-button down and released strictly AFTER
    # the right-button up → held across the whole context_click (the bug: key_up
    # landing on/ before the pointer-up tick).
    assert key_down_i < pointer_down_i
    assert key_up_i > pointer_up_i
    assert key[key_down_i]["value"] == Keys.CONTROL
    assert key[key_up_i]["value"] == Keys.CONTROL


def test_coord_right_click_holds_two_modifiers_across_context_click():
    # Tick padding generalizes to N modifiers (LIFO release, all after pointer-up).
    driver = MagicMock(name="driver")
    do_gesture_at_coordinate(
        driver, 50, 60, {"kind": "right_click"}, ["Control", "Shift"]
    )
    devices = _captured_devices(driver)
    pointer, key = devices["pointer"], devices["key"]
    pointer_up_i = _index_of(pointer, "pointerUp")
    key_ups = [i for i, a in enumerate(key) if a["type"] == "keyUp"]
    assert len(key_ups) == 2
    assert all(i > pointer_up_i for i in key_ups)
    # LIFO: Shift (pressed last) released first.
    shift_up_i = next(i for i, a in enumerate(key)
                      if a["type"] == "keyUp" and a["value"] == Keys.SHIFT)
    ctrl_up_i = next(i for i, a in enumerate(key)
                     if a["type"] == "keyUp" and a["value"] == Keys.CONTROL)
    assert shift_up_i < ctrl_up_i


def test_coord_right_click_meta_aliases_to_control():
    driver = MagicMock(name="driver")
    do_gesture_at_coordinate(driver, 120, 240, {"kind": "right_click"}, ["Meta"])
    key = _captured_devices(driver)["key"]
    assert key[_index_of(key, "keyDown")]["value"] == Keys.CONTROL  # Meta -> CONTROL
    assert key[_index_of(key, "keyUp")]["value"] == Keys.CONTROL


def test_coord_right_click_no_modifiers_touches_no_key_device():
    # Regression: right_click without modifiers stays on the plain pointer path —
    # no key device in the encoded payload at all.
    driver = MagicMock(name="driver")
    do_gesture_at_coordinate(driver, 120, 240, {"kind": "right_click"})
    devices = _captured_devices(driver)
    assert "key" not in devices
    assert any(a["type"] == "pointerDown" for a in devices["pointer"])


def test_coord_long_press_ignores_modifiers():
    # Held keys ride right_click only (spec §2); long_press never holds them.
    driver = MagicMock(name="driver")
    do_gesture_at_coordinate(
        driver, 120, 240, {"kind": "long_press", "duration": 2.0}, ["Control"]
    )
    devices = _captured_devices(driver)
    assert "key" not in devices
    assert any(a["type"] == "pointerDown" for a in devices["pointer"])


def test_coord_runner_threads_held_modifiers_from_ctx():
    from unittest.mock import patch
    from testmu_selenium import _action_click
    driver = MagicMock(name="driver")
    cm = {"kind": "right_click"}
    ctx = {"driver": driver, "click_modifier": cm, "modifiers": ["Control"]}
    with patch.object(_action_click, "resolve_click_modifier_variables", side_effect=lambda d: d), \
         patch.object(_action_click, "validate_click_modifier", side_effect=lambda d: d), \
         patch.object(_action_click, "do_gesture_at_coordinate", return_value=True) as m:
        assert _action_click._click_coord_runner(driver, 120, 240, ctx) is True
    m.assert_called_once_with(driver, 120, 240, cm, ["Control"])
