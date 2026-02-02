from unittest import mock

from bec_lib.bl_conditions import (
    FastOrbitFeedbackCondition,
    LightAvailableCondition,
    ShutterCondition,
)


def test_shutter_condition():
    device = mock.MagicMock()
    shutter_condition = ShutterCondition(device)
    shutter_condition.run()
    device.read.assert_called_once()
    assert shutter_condition.on_failure_msg() == "Check beam failed: Shutter is closed."
    assert shutter_condition.name == "shutter"


def test_light_available_condition():
    device = mock.MagicMock()
    light_available_condition = LightAvailableCondition(device)
    light_available_condition.run()
    device.read.assert_called_once()
    assert light_available_condition.on_failure_msg() == "Check beam failed: Light not available."
    assert light_available_condition.name == "light_available"


def test_fast_orbit_feedback_condition():
    device = mock.MagicMock()
    fast_orbit_feedback_condition = FastOrbitFeedbackCondition(device)
    fast_orbit_feedback_condition.run()
    device.read.assert_called_once()
    assert (
        fast_orbit_feedback_condition.on_failure_msg()
        == "Check beam failed: Fast orbit feedback is not running."
    )
    assert fast_orbit_feedback_condition.name == "fast_orbit_feedback"
