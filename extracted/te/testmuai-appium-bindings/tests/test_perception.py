"""Fresh-perception capture: wire entries + the retained descriptor map."""
from pathlib import Path

import pytest

from testmu_appium._helpers._perception import Perception, capture_perception

_XML = (Path(__file__).resolve().parent / "fixtures" / "page_source_gmail.xml").read_text()


class _FakeDriver:
    page_source = _XML

    def get_window_size(self):
        return {"width": 1080, "height": 2340}

    def get_screenshot_as_png(self):
        return b"\x89PNG-fake"


def test_wire_entries_carry_only_the_documented_keys():
    p = capture_perception(_FakeDriver(), include_screenshot=False)
    assert p.entries
    for entry in p.entries:
        assert set(entry) == {"index", "role", "name", "states", "position_hint"}


def test_wire_entries_are_one_based_and_ordered():
    p = capture_perception(_FakeDriver(), include_screenshot=False)
    assert [e["index"] for e in p.entries] == list(range(1, len(p.entries) + 1))


def test_descriptor_map_is_keyed_by_the_same_index():
    p = capture_perception(_FakeDriver(), include_screenshot=False)
    assert set(p.descriptors) == {e["index"] for e in p.entries}


def test_descriptor_carries_the_source_attributes_needed_for_a_fresh_lookup():
    p = capture_perception(_FakeDriver(), include_screenshot=False)
    compose = next(d for d in p.descriptors.values() if d["content_desc"] == "Compose")
    assert compose["resource_id"] == "com.google.android.gm:id/compose"
    assert compose["text"] == "Compose"
    assert compose["cls"] == "android.widget.Button"
    assert compose["bounds"] == (840, 2050, 1040, 2250)
    assert compose["center"] == (940, 2150)


def test_screenshot_is_base64_when_requested():
    import base64

    p = capture_perception(_FakeDriver(), include_screenshot=True)
    assert base64.b64decode(p.screenshot_b64) == b"\x89PNG-fake"


def test_screenshot_failure_does_not_abort_the_capture():
    class _NoScreenshot(_FakeDriver):
        def get_screenshot_as_png(self):
            raise RuntimeError("screenshot unavailable")

    p = capture_perception(_NoScreenshot(), include_screenshot=True)
    assert p.entries
    assert p.screenshot_b64 is None


def test_empty_page_source_yields_no_entries():
    class _Empty(_FakeDriver):
        page_source = "<hierarchy rotation='0'/>"

    p = capture_perception(_Empty(), include_screenshot=False)
    assert p.entries == []
    assert p.descriptors == {}


def test_perception_records_the_window_it_was_captured_against():
    p = capture_perception(_FakeDriver(), include_screenshot=False)
    assert isinstance(p, Perception)
    assert p.window == (1080, 2340)


class _BlindDriver(_FakeDriver):
    """A driver whose screenshot capture fails."""

    def get_screenshot_as_png(self):
        raise RuntimeError("screencap timed out")


class TestScreenshotFailureMode:
    """Heal's perception is allowed to run without pixels; the vision verb is not.

    A visual read answered from the flat entry list alone is a different question,
    answered against no pixels.
    """

    def test_heal_perception_continues_without_a_screenshot(self):
        p = capture_perception(_BlindDriver())
        assert p.screenshot_b64 is None
        assert p.entries, "the entry list is still what heal reasons from"

    def test_heal_perception_is_the_default(self):
        """require_screenshot defaults off, so no existing caller starts raising."""
        assert capture_perception(_BlindDriver()).screenshot_b64 is None

    def test_requiring_the_screenshot_raises(self):
        from testmu_appium._errors import ScreenshotUnavailable

        with pytest.raises(ScreenshotUnavailable) as exc:
            capture_perception(_BlindDriver(), require_screenshot=True)
        assert "screencap timed out" in str(exc.value)

    def test_requiring_a_screenshot_that_succeeds_returns_it(self):
        p = capture_perception(_FakeDriver(), require_screenshot=True)
        assert p.screenshot_b64

    def test_a_skipped_capture_is_not_a_failure_even_when_required(self):
        """include_screenshot=False means the caller did not want one at all."""
        p = capture_perception(
            _BlindDriver(), include_screenshot=False, require_screenshot=True
        )
        assert p.screenshot_b64 is None


class TestCaptureFollowsTheConfiguredPlatform:
    """Heal and vision read THIS capture. When it parsed through the Android
    module directly, a configured-iOS session healed against zero rows while
    the public dispatcher saw the controls fine — same driver, same XML."""

    _IOS_XML = (
        '<AppiumAUT><XCUIElementTypeApplication type="XCUIElementTypeApplication"'
        ' name="Demo" enabled="true" visible="true" accessible="false"'
        ' x="0" y="0" width="414" height="896">'
        '<XCUIElementTypeButton type="XCUIElementTypeButton" name="Sign in"'
        ' label="Sign in" enabled="true" visible="true" accessible="true"'
        ' x="100" y="400" width="200" height="44"/>'
        "</XCUIElementTypeApplication></AppiumAUT>"
    )

    class _IosDriver:
        page_source = None  # set per test

        def get_window_size(self):
            return {"width": 414, "height": 896}

    def test_a_configured_ios_session_captures_ios_rows(self, monkeypatch):
        from testmu_appium import _config

        monkeypatch.setitem(_config._config, "platform", "ios")
        driver = self._IosDriver()
        driver.page_source = self._IOS_XML
        p = capture_perception(driver, include_screenshot=False)
        assert [e["name"] for e in p.entries] == ["Sign in"]

    def test_android_remains_the_default(self, monkeypatch):
        from testmu_appium import _config

        monkeypatch.setitem(_config._config, "platform", "android")
        p = capture_perception(_FakeDriver(), include_screenshot=False)
        assert p.entries, "the Android fixture must still parse"


class TestElementSnapshot:
    """The analyzer's single-element snapshot, built from a retained descriptor."""

    def _snapshot_for(self, content_desc):
        from testmu_appium._helpers._perception import element_snapshot

        p = capture_perception(_FakeDriver(), include_screenshot=False)
        index = next(
            i for i, d in p.descriptors.items() if d.get("content_desc") == content_desc
        )
        return element_snapshot(p, index)

    def test_it_carries_exactly_the_keys_the_analyzer_reads(self):
        snapshot = self._snapshot_for("Compose")
        assert set(snapshot) == {
            "tag_name", "text_content", "attributes", "styles", "states",
        }

    def test_tag_name_is_the_android_class(self):
        assert self._snapshot_for("Compose")["tag_name"].startswith("android.")

    def test_source_attributes_ride_under_their_android_names(self):
        attributes = self._snapshot_for("Compose")["attributes"]
        assert attributes["content-desc"] == "Compose"
        assert "resource-id" in attributes

    def test_styles_are_empty_because_native_has_no_computed_style(self):
        assert self._snapshot_for("Compose")["styles"] == {}

    def test_states_come_from_the_wire_entry(self):
        from testmu_appium._helpers._perception import Perception, element_snapshot

        perception = Perception(
            entries=[{"index": 1, "role": "checkbox", "name": "Agree",
                      "states": ["checked", "enabled"], "position_hint": "top-left"}],
            descriptors={1: {"cls": "android.widget.CheckBox", "text": "Agree"}},
        )
        assert element_snapshot(perception, 1)["states"] == {
            "checked": True, "enabled": True,
        }

    def test_text_content_falls_back_to_the_entry_name(self):
        from testmu_appium._helpers._perception import Perception, element_snapshot

        perception = Perception(
            entries=[{"index": 1, "role": "button", "name": "Send",
                      "states": [], "position_hint": ""}],
            descriptors={1: {"cls": "android.widget.Button", "text": ""}},
        )
        assert element_snapshot(perception, 1)["text_content"] == "Send"

    def test_an_absent_index_yields_the_empty_snapshot_rather_than_raising(self):
        from testmu_appium._helpers._perception import Perception, element_snapshot

        snapshot = element_snapshot(Perception(), 99)
        assert snapshot["tag_name"] == "" and snapshot["attributes"] == {}
