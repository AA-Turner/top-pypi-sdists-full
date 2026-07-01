"""Smoke tests for relocated runtime helpers."""
from unittest.mock import MagicMock, patch

import pytest


def test_clear_element_imports():
    from testmu_selenium._helpers import clear_element
    assert clear_element is not None


def test_load_test_config_exported_at_top_level():
    """Exported tests call testmu_selenium.load_test_config() to merge per-run
    (data-driven) test_params before configure(); it must be importable from
    the package root."""
    import testmu_selenium
    assert callable(testmu_selenium.load_test_config)


def test_dom_wait_imports():
    from testmu_selenium._helpers import dom_wait
    assert dom_wait is not None


def test_driver_imports():
    from testmu_selenium._helpers import driver
    assert driver is not None


def test_execute_js_imports():
    from testmu_selenium._helpers import execute_js
    assert execute_js is not None


def test_js_templates_imports():
    from testmu_selenium._helpers import js_templates
    assert js_templates is not None


def test_vision_query_imports():
    from testmu_selenium._helpers import vision_query
    assert vision_query is not None


def test_input_value_imports():
    from testmu_selenium._helpers import input_value
    assert input_value is not None


class TestExecuteJSSmoke:
    """Verify executeJS wraps user code and returns the result envelope."""

    def test_executeJS_returns_value_envelope_on_success(self):
        from testmu_selenium._helpers.execute_js import executeJS

        mock_driver = MagicMock()
        mock_driver.execute_script.return_value = "ok"

        result = executeJS(mock_driver, "return 1;")

        assert mock_driver.execute_script.called
        assert isinstance(result, dict)
        assert result["value"] == "ok"
        assert result["error"] == ""
        assert result["line"] is None

    def test_executeJS_returns_error_envelope_on_js_error_dict(self):
        from testmu_selenium._helpers.execute_js import executeJS

        mock_driver = MagicMock()
        mock_driver.execute_script.return_value = {
            "error": "ReferenceError: foo is not defined\n    at <anonymous>:3:1"
        }

        result = executeJS(mock_driver, "foo();")

        assert result["value"] == ""
        assert "ReferenceError" in result["error"]
        assert result["line"] == 3

    def test_executeJS_logs_result_value_on_success(self, caplog):
        """The JS return value must be surfaced in the step log so it shows up
        on the LambdaTest automation dashboard (parity with execute_db/api)."""
        import logging

        from testmu_selenium._helpers.execute_js import executeJS

        mock_driver = MagicMock()
        mock_driver.execute_script.return_value = "hello-result"

        with caplog.at_level(logging.INFO, logger="testmu_selenium._helpers.execute_js"):
            executeJS(mock_driver, "return 'hello-result';")

        result_lines = [r.getMessage() for r in caplog.records if "[execute_js] result=" in r.getMessage()]
        assert result_lines, "expected an '[execute_js] result=' log line"
        assert "hello-result" in result_lines[0]


class TestExecuteJSVariableInjection:
    """executeJS must inject _variable_store entries as JS const declarations
    so a JS step can reference prior variables (e.g. an API-call result),
    matching the Playwright execute_js runtime. See _vars._variable_store."""

    def setup_method(self):
        from testmu_selenium import _vars
        _vars._variable_store.clear()

    def teardown_method(self):
        from testmu_selenium import _vars
        _vars._variable_store.clear()

    def test_executeJS_injects_store_var_as_const(self):
        from testmu_selenium import _vars
        from testmu_selenium._helpers.execute_js import executeJS

        _vars.set_var(
            "api_variable22ec",
            {"response_body": {"results": [{"email": "real@example.com"}]}},
        )

        mock_driver = MagicMock()
        mock_driver.execute_script.return_value = "ok"

        executeJS(mock_driver, "return {api_variable22ec};")

        script = mock_driver.execute_script.call_args[0][0]
        assert "const api_variable22ec =" in script
        assert "real@example.com" in script

    def test_executeJS_skips_non_identifier_store_keys(self):
        from testmu_selenium import _vars
        from testmu_selenium._helpers.execute_js import executeJS

        _vars.set_var("not.an.ident", "skip-me")

        mock_driver = MagicMock()
        mock_driver.execute_script.return_value = "ok"

        executeJS(mock_driver, "return 1;")

        script = mock_driver.execute_script.call_args[0][0]
        assert "not.an.ident" not in script


class TestVisionQuerySmoke:
    def test_visionQuery_callable(self):
        from testmu_selenium._helpers.vision_query import visionQuery
        assert callable(visionQuery)


# ---------------------------------------------------------------------------
# visionQuery — replaces the deleted stub-returns-True smoke test.
# Covers: success paths (bool/number/str), driver-override path, and the three
# failure modes that turn into RuntimeError (None response, error response,
# missing 'vision_query' field).
# ---------------------------------------------------------------------------


def _patch_vq_helpers(json_response):
    """Patch SmartWait + get_driver + Heal so visionQuery runs without a live session.

    Heal.vision_query() returns an object whose .json() yields ``json_response``.
    Returns a context-manager-like tuple of patches; callers use it as a multi-with.
    """
    sw_inst = MagicMock(name="SmartWait-inst")
    driver = MagicMock(name="driver")
    return (
        patch("testmu_selenium._helpers.vision_query.SmartWait", return_value=sw_inst),
        patch("testmu_selenium._helpers.vision_query.get_driver", return_value=driver),
        patch("testmu_selenium._helpers.vision_query.Heal"),
        json_response,
    )


@pytest.mark.parametrize(
    "raw,return_type,expected",
    [
        # bool — native JSON bool
        (True, "bool", True),
        (False, "bool", False),
        # bool — string fallbacks (endpoint may stringify)
        ("true", "bool", True),
        ("YES", "bool", True),
        ("1", "bool", True),
        ("false", "bool", False),
        ("no", "bool", False),
        ("", "bool", False),
        # number — native JSON numeric
        (42, "number", 42.0),
        (3.14, "number", 3.14),
        # number — string fallback
        ("12.5", "number", 12.5),
        # number — junk-stripping fallback (digits + dot survive)
        ("price: $99.99 USD", "number", 99.99),
        # number — empty/garbage → 0.0
        ("", "number", 0.0),
        ("nothing numeric", "number", 0.0),
        # str — anything coerces to str; None → ""
        ("hello", "str", "hello"),
        (123, "str", "123"),
        (None, "str", ""),
    ],
)
def test_visionQuery_cast_value(raw, return_type, expected):
    """_cast_value: the cast layer between JSON response and caller's typed result.

    Table covers all three return_type branches plus the string-fallback paths
    that handle endpoints stringifying their answer.
    """
    from testmu_selenium._helpers.vision_query import _cast_value
    assert _cast_value(raw, return_type) == expected


class TestVisionQueryFlow:
    """End-to-end visionQuery with Heal/SmartWait/get_driver mocked."""

    def test_returns_cast_bool(self):
        sw, gd, heal, _ = _patch_vq_helpers({"vision_query": True})
        with sw, gd, heal as m_heal:
            m_heal.return_value.vision_query.return_value.json.return_value = {"vision_query": True}
            from testmu_selenium._helpers.vision_query import visionQuery
            assert visionQuery("Is X visible?", "bool") is True

    def test_returns_cast_number(self):
        sw, gd, heal, _ = _patch_vq_helpers({"vision_query": 7})
        with sw, gd, heal as m_heal:
            m_heal.return_value.vision_query.return_value.json.return_value = {"vision_query": 7}
            from testmu_selenium._helpers.vision_query import visionQuery
            assert visionQuery("How many?", "number") == 7.0

    def test_returns_cast_str(self):
        sw, gd, heal, _ = _patch_vq_helpers({"vision_query": "hello"})
        with sw, gd, heal as m_heal:
            m_heal.return_value.vision_query.return_value.json.return_value = {"vision_query": "hello"}
            from testmu_selenium._helpers.vision_query import visionQuery
            assert visionQuery("Read the label", "str") == "hello"

    def test_driver_override_skips_get_driver(self):
        """When driver is passed explicitly, get_driver must not be called —
        the verb is callable without an active testmu_selenium.run() session."""
        explicit_driver = MagicMock(name="explicit-driver")
        with patch("testmu_selenium._helpers.vision_query.SmartWait", return_value=MagicMock()), \
             patch("testmu_selenium._helpers.vision_query.get_driver") as m_get_driver, \
             patch("testmu_selenium._helpers.vision_query.Heal") as m_heal:
            m_heal.return_value.vision_query.return_value.json.return_value = {"vision_query": True}
            from testmu_selenium._helpers.vision_query import visionQuery
            visionQuery("Is X visible?", "bool", driver=explicit_driver)
        m_get_driver.assert_not_called()

    def test_raises_when_response_is_none(self):
        with patch("testmu_selenium._helpers.vision_query.SmartWait", return_value=MagicMock()), \
             patch("testmu_selenium._helpers.vision_query.get_driver", return_value=MagicMock()), \
             patch("testmu_selenium._helpers.vision_query.Heal") as m_heal:
            m_heal.return_value.vision_query.return_value = None
            from testmu_selenium._helpers.vision_query import visionQuery
            with pytest.raises(RuntimeError, match="no response"):
                visionQuery("Is X visible?", "bool")

    def test_raises_when_response_has_error(self):
        with patch("testmu_selenium._helpers.vision_query.SmartWait", return_value=MagicMock()), \
             patch("testmu_selenium._helpers.vision_query.get_driver", return_value=MagicMock()), \
             patch("testmu_selenium._helpers.vision_query.Heal") as m_heal:
            m_heal.return_value.vision_query.return_value.json.return_value = {"error": "model timeout"}
            from testmu_selenium._helpers.vision_query import visionQuery
            with pytest.raises(RuntimeError, match="model timeout"):
                visionQuery("Is X visible?", "bool")

    def test_raises_when_vision_query_field_missing(self):
        """Response with neither 'error' nor 'vision_query' is malformed; verb
        must raise rather than silently return None/empty."""
        with patch("testmu_selenium._helpers.vision_query.SmartWait", return_value=MagicMock()), \
             patch("testmu_selenium._helpers.vision_query.get_driver", return_value=MagicMock()), \
             patch("testmu_selenium._helpers.vision_query.Heal") as m_heal:
            m_heal.return_value.vision_query.return_value.json.return_value = {"unexpected": "shape"}
            from testmu_selenium._helpers.vision_query import visionQuery
            with pytest.raises(RuntimeError, match="missing 'vision_query'"):
                visionQuery("Is X visible?", "bool")

    def test_smart_wait_called_with_is_vision_true(self):
        """Vision queries must use the vision smart-wait variant — distinct from
        is_vision=False used by element actions, because vision tier latency
        budget differs."""
        sw_inst = MagicMock(name="SmartWait-inst")
        with patch("testmu_selenium._helpers.vision_query.SmartWait", return_value=sw_inst), \
             patch("testmu_selenium._helpers.vision_query.get_driver", return_value=MagicMock()), \
             patch("testmu_selenium._helpers.vision_query.Heal") as m_heal:
            m_heal.return_value.vision_query.return_value.json.return_value = {"vision_query": True}
            from testmu_selenium._helpers.vision_query import visionQuery
            visionQuery("Is X visible?", "bool")
        sw_inst.smart_wait.assert_called_once_with(is_vision=True)


class TestJsTemplatesSmoke:
    def test_scroll_js_class_exposes_static_helpers(self):
        from testmu_selenium._helpers.js_templates import ScrollJS

        js = ScrollJS.scroll_by("10", "20")
        assert "scrollBy(10, 20)" in js

    def test_shadow_dom_js_get_shadow_root_child(self):
        from testmu_selenium._helpers.js_templates import ShadowDomJS

        assert "shadowRoot" in ShadowDomJS.get_shadow_root_child()


class TestDomWaitSmoke:
    def test_wait_for_dom_invokes_execute_script(self):
        from testmu_selenium._helpers.dom_wait import wait_for_dom

        mock_driver = MagicMock()
        # WebDriverWait(...).until(lambda d: d.execute_script(...)) — make
        # the predicate truthy on first poll.
        mock_driver.execute_script.return_value = True

        result = wait_for_dom(mock_driver, timeout=1)
        assert result is True
        assert mock_driver.execute_script.called


class TestClearElementSmoke:
    def test_clear_element_backspaces_existing_value(self):
        from testmu_selenium._helpers.clear_element import clear_element

        mock_driver = MagicMock()
        mock_element = MagicMock()
        # First call: return "abc" (the value attr).  Second call: contenteditable
        # attribute lookup.
        mock_element.get_attribute.side_effect = ["abc", "false"]

        clear_element(mock_driver, mock_element)

        # Backspace should be sent len("abc") == 3 times.
        assert mock_element.send_keys.call_count == 3
