"""ship the interacted element's rect for screenshot annotation.

The instance view draws a marker over the element a step acted on; it gets that
rect from the ``lambda-element-bounds`` hook, emitted just before the verb runs.
Without it the run UI has nothing to annotate ("Incorrect Screenshot displayed
while re-authoring the test").

The rect must be in MAIN-PAGE coordinates: element.rect is relative to the
element's own document, so an element inside an iframe would be annotated at the
wrong place on a top-level screenshot.
"""
import json
from unittest.mock import MagicMock, patch

import pytest

from testmu_selenium._helpers import element_bounds as eb


@pytest.fixture(autouse=True)
def _cloud():
    with patch("testmu_selenium._config.run_target", "cloud"):
        yield


def _emitted(driver):
    """The lambda-element-bounds payloads this driver was asked to execute."""
    out = []
    for call in driver.execute_script.call_args_list:
        script = call.args[0] if call.args else ""
        if isinstance(script, str) and script.startswith("lambda-element-bounds="):
            out.append(json.loads(script.split("=", 1)[1]))
    return out


class TestSendElementBounds:
    def test_emits_the_main_page_rect(self):
        driver = MagicMock()
        driver.execute_script.return_value = {"x": 10, "y": 20, "width": 30, "height": 40}
        eb.send_element_bounds(driver, MagicMock())
        assert _emitted(driver) == [{"x": 10, "y": 20, "width": 30, "height": 40}]

    def test_walks_the_frame_chain(self):
        """The JS must add each frame owner's offset, not just the local rect."""
        assert "frameElement" in eb._MAIN_PAGE_RECT_JS
        assert "win.parent" in eb._MAIN_PAGE_RECT_JS

    def test_falls_back_to_element_rect_when_the_script_fails(self):
        driver = MagicMock()
        element = MagicMock()
        element.rect = {"x": 1, "y": 2, "width": 3, "height": 4}

        def _script(script, *args):
            if script is eb._MAIN_PAGE_RECT_JS:
                raise RuntimeError("no javascript for you")
            return None

        driver.execute_script.side_effect = _script
        eb.send_element_bounds(driver, element)
        assert _emitted(driver) == [{"x": 1, "y": 2, "width": 3, "height": 4}]

    def test_silent_when_both_rect_sources_fail(self):
        driver = MagicMock()
        element = MagicMock()
        driver.execute_script.side_effect = RuntimeError("boom")
        type(element).rect = property(lambda self: (_ for _ in ()).throw(RuntimeError("boom")))
        eb.send_element_bounds(driver, element)  # must not raise
        assert _emitted(driver) == []

    def test_none_driver_or_element_is_a_no_op(self):
        eb.send_element_bounds(None, MagicMock())
        driver = MagicMock()
        eb.send_element_bounds(driver, None)
        driver.execute_script.assert_not_called()

    def test_instruction_id_rides_along_when_a_step_is_active(self):
        from testmu_selenium._step import step
        driver = MagicMock()
        driver.execute_script.return_value = {"x": 0, "y": 0, "width": 1, "height": 1}
        with patch("testmu_selenium._step._emit_step_hook"):
            with step("s", instruction_id="iid-9"):
                eb.send_element_bounds(driver, MagicMock())
        assert _emitted(driver)[0]["instructionId"] == "iid-9"

    def test_no_instruction_id_key_outside_a_step(self):
        driver = MagicMock()
        driver.execute_script.return_value = {"x": 0, "y": 0, "width": 1, "height": 1}
        eb.send_element_bounds(driver, MagicMock())
        assert "instructionId" not in _emitted(driver)[0]


class TestSendPointBounds:
    def test_coordinate_click_reports_a_zero_size_point(self):
        """The coordinate tier healed to a pixel — there is no box to draw."""
        driver = MagicMock()
        eb.send_point_bounds(driver, 388, 202)
        assert _emitted(driver) == [{"x": 388, "y": 202, "width": 0, "height": 0}]

    def test_none_driver_is_a_no_op(self):
        eb.send_point_bounds(None, 1, 2)  # must not raise


class TestRunTargetGate:
    def test_local_run_emits_nothing(self):
        driver = MagicMock()
        driver.execute_script.return_value = {"x": 0, "y": 0, "width": 1, "height": 1}
        with patch("testmu_selenium._config.run_target", "local"):
            eb.send_element_bounds(driver, MagicMock())
            eb.send_point_bounds(driver, 1, 2)
        assert _emitted(driver) == []
