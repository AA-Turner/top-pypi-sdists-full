"""vision_query() — screenshot read via POST /api/v1/analyzer, type "visual"."""
import json
from pathlib import Path

import httpx
import pytest
import respx

from testmu_appium import _config
from testmu_appium._errors import TestmuConfigError
from testmu_appium._helpers.vision_query import vision_query
from testmu_appium._vars import _variable_store, clear_state, set_var

_XML = (Path(__file__).resolve().parent / "fixtures" / "page_source_gmail.xml").read_text()
_URL = "https://ai.example.test/v16-server/api/v1/analyzer"


class _FakeDriver:
    page_source = _XML

    def get_window_size(self):
        return {"width": 1080, "height": 2340}

    def get_screenshot_as_png(self):
        return b"\x89PNG-fake"


@pytest.fixture(autouse=True)
def _env(monkeypatch):
    monkeypatch.setenv("TESTMU_AI_API_HOST", "https://ai.example.test/v16-server")
    monkeypatch.setattr(_config, "smart", True)
    clear_state()
    yield
    clear_state()


@respx.mock
def test_returns_the_extracted_value_as_a_string():
    respx.post(_URL).mock(return_value=httpx.Response(200, json={"extracted_value": "true"}))
    result = vision_query(_FakeDriver(), query="Is the FAB visible?")
    assert result == "true"


@respx.mock
def test_request_body_carries_the_visual_type_query_and_screenshot():
    route = respx.post(_URL).mock(return_value=httpx.Response(200, json={"extracted_value": "x"}))
    vision_query(_FakeDriver(), query="what colour is the FAB?")
    payload = json.loads(route.calls[0].request.content)
    assert payload["type"] == "visual"
    assert payload["query"] == "what colour is the FAB?"
    assert payload["screenshot_b64"]


@respx.mock
def test_the_entry_list_stays_off_a_visual_request():
    """The analyzer's visual leg reads the pixels; a flat entry list is ignored."""
    route = respx.post(_URL).mock(return_value=httpx.Response(200, json={"extracted_value": "x"}))
    vision_query(_FakeDriver(), query="q")
    assert "full_dom_list" not in json.loads(route.calls[0].request.content)


@respx.mock
def test_output_variable_is_written():
    respx.post(_URL).mock(return_value=httpx.Response(200, json={"extracted_value": "red"}))
    result = vision_query(_FakeDriver(), query="q", output_variable="fab_colour")
    assert _variable_store["fab_colour"] == result == "red"


@respx.mock
def test_analyzer_abstention_raises_without_overwriting_the_output_variable():
    set_var("fab_colour", "previous")
    respx.post(_URL).mock(
        return_value=httpx.Response(200, json={"extracted_value": "__not_visible__"})
    )

    with pytest.raises(RuntimeError, match="current screenshot"):
        vision_query(_FakeDriver(), query="q", output_variable="fab_colour")

    assert _variable_store["fab_colour"] == "previous"


@respx.mock
def test_query_resolves_variable_tokens():
    set_var("target", "the FAB")
    route = respx.post(_URL).mock(return_value=httpx.Response(200, json={"extracted_value": "x"}))
    vision_query(_FakeDriver(), query="describe {{target}}")
    body = json.loads(route.calls[0].request.content)
    assert body["query"] == "describe the FAB"


def test_smart_disabled_raises_config_error(monkeypatch):
    monkeypatch.setattr(_config, "smart", False)
    with pytest.raises(TestmuConfigError) as exc:
        vision_query(_FakeDriver(), query="q")
    assert "TESTMU_SMART" in str(exc.value)


@respx.mock
def test_non_200_response_raises_naming_the_endpoint():
    respx.post(_URL).mock(return_value=httpx.Response(500, text="boom"))
    with pytest.raises(RuntimeError) as exc:
        vision_query(_FakeDriver(), query="q")
    assert "vision_query" in str(exc.value)


@respx.mock
def test_malformed_body_missing_extracted_value_raises():
    respx.post(_URL).mock(return_value=httpx.Response(200, json={"unexpected": "shape"}))
    with pytest.raises(RuntimeError) as exc:
        vision_query(_FakeDriver(), query="q")
    assert "extracted_value" in str(exc.value)


@respx.mock
def test_non_json_response_body_raises():
    respx.post(_URL).mock(return_value=httpx.Response(200, text="<html>gateway</html>"))
    with pytest.raises(RuntimeError):
        vision_query(_FakeDriver(), query="q")


class TestScreenshotIsARequirement:
    """This verb reads a value off the PIXELS. Silently answering from the flat
    entry list alone returns a different question's answer as though it were this
    one's — so a lost capture raises here, while heal's perception stays fail-open."""

    class _Blind(_FakeDriver):
        def get_screenshot_as_png(self):
            raise RuntimeError("screencap timed out")

    @respx.mock
    def test_a_failed_capture_raises(self):
        from testmu_appium._errors import ScreenshotUnavailable

        route = respx.post(_URL).mock(
            return_value=httpx.Response(200, json={"extracted_value": "true"})
        )
        with pytest.raises(ScreenshotUnavailable):
            vision_query(self._Blind(), query="Is the FAB visible?")
        assert not route.called, "no request may go out without the pixels"

    @respx.mock
    def test_heals_perception_is_unaffected(self, monkeypatch):
        """The fail-open path stays fail-open: heal is a recovery path that is
        allowed to run degraded rather than not at all."""
        from testmu_appium._helpers._perception import capture_perception

        assert capture_perception(self._Blind()).screenshot_b64 is None


class TestDescriptionIsReal:
    """`description` is logged with every line for the call, and defaults to the
    resolved query, so no read is anonymous in the log."""

    @respx.mock
    def test_an_explicit_description_reaches_the_log(self, caplog):
        import logging

        caplog.set_level(logging.INFO, logger="testmu_appium")
        respx.post(_URL).mock(
            return_value=httpx.Response(200, json={"extracted_value": "3"})
        )
        vision_query(
            _FakeDriver(), query="the badge count", description="check the cart badge"
        )
        assert "check the cart badge" in caplog.text

    @respx.mock
    def test_an_empty_description_defaults_to_the_resolved_query(self, caplog):
        import logging

        caplog.set_level(logging.INFO, logger="testmu_appium")
        set_var("item", "socks")
        respx.post(_URL).mock(
            return_value=httpx.Response(200, json={"extracted_value": "yes"})
        )
        vision_query(_FakeDriver(), query="is {{item}} in the cart")
        assert "is socks in the cart" in caplog.text

    @respx.mock
    def test_the_description_does_not_leak_onto_the_request(self):
        """It is a local label. The endpoint's schema is not widened for it."""
        route = respx.post(_URL).mock(
            return_value=httpx.Response(200, json={"extracted_value": "x"})
        )
        vision_query(_FakeDriver(), query="q", description="a label")
        assert "description" not in json.loads(route.calls[0].request.content)
