"""get_vision_coordinates — resolve a description to a point on the live screen.

The mobile twin of the playwright binding's helper. It exists so a recording that
was grounded by VISION can be re-grounded the same way at replay: a screen the
accessibility tree never described has no selector to fall back to, and a
recorded ratio describes a layout that may have moved.
"""
import io

import pytest
from PIL import Image

from testmu_appium import _config
from testmu_appium._errors import TestmuConfigError, UnsupportedOnPlatform
from testmu_appium._helpers import _adapters
from testmu_appium._helpers.vision_coordinates import get_vision_coordinates


def _frame(width, height):
    buffer = io.BytesIO()
    Image.new("RGB", (width, height)).save(buffer, format="JPEG")
    return buffer.getvalue()


class _Driver:
    """A device whose screenshot arrives at half size.

    Measured, not invented: UiAutomator2's MJPEG server serves this 1080x2400
    device at 540x1200. The mismatch is deliberate here — the point of these
    tests is that it does not have to be corrected for.
    """

    def get_window_size(self):
        return {"width": 1080, "height": 2400}

    def get_screenshot_as_png(self):
        return _frame(540, 1200)

    @property
    def orientation(self):
        return "PORTRAIT"

    @property
    def page_source(self):
        return "<hierarchy></hierarchy>"


class _Response:
    def __init__(self, payload, status=200):
        self._payload = payload
        self.status_code = status
        self.text = str(payload)

    def json(self):
        return self._payload


@pytest.fixture(autouse=True)
def _smart_on(monkeypatch):
    monkeypatch.setattr(_config, "smart_enabled", lambda: True)


def _patch_post(monkeypatch, response):
    sent = {}

    def _fake(method, url, **kwargs):
        sent["url"] = url
        sent["body"] = kwargs.get("json_data")
        return response

    monkeypatch.setattr(
        "testmu_appium._helpers.vision_coordinates.request_with_retry", _fake
    )
    return sent


def test_a_located_element_comes_back_as_a_point(monkeypatch):
    sent = _patch_post(monkeypatch, _Response({"found": True, "x": 540, "y": 1200}))
    assert get_vision_coordinates(_Driver(), "the orange Drag me chip") == (540, 1200)
    assert sent["url"].endswith("/api/v1/vision/coordinates")


def test_the_request_asks_for_an_answer_in_device_pixels(monkeypatch):
    """The endpoint answers in the width and height it is GIVEN, not in the
    screenshot's own pixels — verified against the live service, which placed one
    unchanged screen at the same relative point when declared at 100x100, at
    540x1200 and at 1080x2400.

    So the MJPEG stream's downscaling (0.5, declared on the android row of the
    ``screenshot_scaling`` registry) needs no correction: the caller acts through
    Appium in device pixels, so the android row's basis asks in them.
    """
    sent = _patch_post(monkeypatch, _Response({"found": True, "x": 1, "y": 2}))
    get_vision_coordinates(_Driver(), "anything")
    assert sent["body"]["width"] == 1080
    assert sent["body"]["height"] == 2400
    assert sent["body"]["action_instruction"] == "anything"
    assert sent["body"]["screenshot_b64"]


def test_the_answer_is_used_as_given(monkeypatch):
    """No rescaling of any kind. A point returned against declared device
    dimensions is already where Appium must touch."""
    _patch_post(monkeypatch, _Response({"found": True, "x": 542, "y": 2034}))
    assert get_vision_coordinates(_Driver(), "anything") == (542, 2034)


def test_an_element_the_model_cannot_find_raises_rather_than_guessing(monkeypatch):
    """No fallback to a recorded point: this helper is reached BECAUSE the other
    ways of finding the element are gone."""
    _patch_post(monkeypatch, _Response({"found": False}))
    with pytest.raises(RuntimeError, match="not found"):
        get_vision_coordinates(_Driver(), "a control that is not there")


def test_a_non_200_is_an_error_not_an_empty_answer(monkeypatch):
    _patch_post(monkeypatch, _Response({}, status=502))
    with pytest.raises(RuntimeError, match="502"):
        get_vision_coordinates(_Driver(), "anything")


def test_smart_off_refuses_because_there_is_no_local_answer(monkeypatch):
    monkeypatch.setattr(_config, "smart_enabled", lambda: False)
    with pytest.raises(TestmuConfigError):
        get_vision_coordinates(_Driver(), "anything")


def test_an_unshipped_platform_raises_and_never_reaches_the_endpoint(monkeypatch):
    """The refusal now fires at PERCEPTION, one step earlier than the
    coordinate-basis row: capture routes through the platform dispatcher, and a
    platform with no parser cannot even read the screen it would ground on."""
    monkeypatch.setitem(_config._config, "platform", "tizen")
    sent = _patch_post(monkeypatch, _Response({"found": True, "x": 1, "y": 2}))
    with pytest.raises(UnsupportedOnPlatform) as exc:
        get_vision_coordinates(_Driver(), "anything")
    assert "tizen" in str(exc.value)
    assert sent == {}


def test_both_registry_rows_carry_the_vision_window_entry():
    for platform in ("android", "ios"):
        assert "vision_window" in _adapters._REGISTRIES["screenshot_scaling"][platform]


def test_the_ios_basis_is_points_which_is_what_the_window_reports(monkeypatch):
    """Deliberately the same driver call as Android's, in a different unit. Ask in
    points and act in points, and the screenshot's larger pixel resolution never
    enters the calculation."""
    monkeypatch.setitem(_config._config, "platform", "ios")
    from testmu_appium._helpers.vision_coordinates import _window
    # Whatever the driver reports IS the basis — on iOS that report is in points.
    assert _window(_Driver()) == (1080, 2400)
