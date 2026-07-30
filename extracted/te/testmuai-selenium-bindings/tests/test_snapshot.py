"""Focused snapshot routing and provisioned-runtime contract tests."""

from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest
from selenium.common.exceptions import JavascriptException, WebDriverException

from testmu_selenium import _action_textual_query as textual_action
from testmu_selenium._helpers import snapshot


# Deliberately tiny public-domain-style test stub; no production extractor bytes.
_STUB_SOURCE = "globalThis.__snapshotTestStub = true;"


def _valid_snapshots(node_count=1):
    parent_index = [-1] + ([0] * (node_count - 1))
    return {
        "a11y_snapshot": {"nodes": []},
        "dom_snapshot": {
            "documents": [{
                "nodes": {
                    "nodeName": [0] * node_count,
                    "nodeType": [1] * node_count,
                    "nodeValue": [0] * node_count,
                    "attributes": [[] for _ in range(node_count)],
                    "parentIndex": parent_index,
                },
                "layout": {"nodeIndex": [], "styles": [], "bounds": []},
            }],
            "strings": ["html"],
        },
    }


@pytest.fixture(autouse=True)
def _clear_runtime_cache():
    snapshot._load_runtime_source.cache_clear()
    yield
    snapshot._load_runtime_source.cache_clear()


@pytest.mark.parametrize("capabilities", [
    {"platformName": "iOS", "browserName": "Safari"},
    {"platformName": "macOS", "browserName": "safari"},
    {"platformName": "linux", "browserName": "Firefox"},
])
def test_non_cdp_platforms_route_to_runtime(monkeypatch, capabilities):
    driver = MagicMock(capabilities=capabilities)
    runtime = MagicMock(return_value=({"nodes": []}, _valid_snapshots()["dom_snapshot"]))
    cdp = MagicMock(side_effect=AssertionError("CDP must not be called"))
    monkeypatch.setattr(snapshot, "_capture_runtime_snapshot", runtime)
    monkeypatch.setattr(snapshot, "_capture_cdp_snapshot", cdp)

    assert snapshot.capture_a11y_dom_snapshot(driver) == (
        {"nodes": []}, _valid_snapshots()["dom_snapshot"], None,
    )
    runtime.assert_called_once_with(driver)
    cdp.assert_not_called()


@pytest.mark.parametrize("capabilities", [
    {"platformName": "linux", "browserName": "chrome"},
    {"platformName": "Android", "browserName": "chrome"},
])
def test_chrome_and_android_preserve_cdp_route(monkeypatch, capabilities):
    driver = MagicMock(capabilities=capabilities)
    cdp = MagicMock(return_value=({"nodes": []}, _valid_snapshots()["dom_snapshot"]))
    runtime = MagicMock(side_effect=AssertionError("runtime must not be called"))
    monkeypatch.setattr(snapshot, "_capture_cdp_snapshot", cdp)
    monkeypatch.setattr(snapshot, "_capture_runtime_snapshot", runtime)

    snapshot.capture_a11y_dom_snapshot(driver)

    cdp.assert_called_once_with(driver)
    runtime.assert_not_called()


def test_unknown_engine_falls_back_only_for_explicit_unsupported_cdp(monkeypatch):
    driver = MagicMock(capabilities={"platformName": "linux", "browserName": "webkit"})
    monkeypatch.setattr(
        snapshot, "_capture_cdp_snapshot",
        MagicMock(side_effect=WebDriverException("unknown command: CDP endpoint unavailable")),
    )
    runtime = MagicMock(return_value=({"nodes": []}, _valid_snapshots()["dom_snapshot"]))
    monkeypatch.setattr(snapshot, "_capture_runtime_snapshot", runtime)

    snapshot.capture_a11y_dom_snapshot(driver)

    runtime.assert_called_once_with(driver)


def test_unknown_engine_falls_back_from_raw_unknown_command_envelope(monkeypatch):
    driver = MagicMock()
    driver.capabilities = {"platformName": "linux", "browserName": "webkit"}
    driver.session_id = "session-id"
    driver.command_executor._url = "https://grid.example"
    driver.command_executor._request.return_value = {
        "value": {"error": "unknown command", "message": "CDP route is unavailable"},
    }
    runtime = MagicMock(return_value=({"nodes": []}, _valid_snapshots()["dom_snapshot"]))
    monkeypatch.setattr(snapshot, "_capture_runtime_snapshot", runtime)

    snapshot.capture_a11y_dom_snapshot(driver)

    driver.command_executor._request.assert_called_once()
    runtime.assert_called_once_with(driver)


def test_unknown_engine_propagates_other_raw_remote_error_envelope(monkeypatch):
    driver = MagicMock()
    driver.capabilities = {"platformName": "linux", "browserName": "webkit"}
    driver.session_id = "session-id"
    driver.command_executor._url = "https://grid.example"
    driver.command_executor._request.return_value = {
        "value": {"error": "invalid session id", "message": "session disconnected"},
    }
    runtime = MagicMock()
    monkeypatch.setattr(snapshot, "_capture_runtime_snapshot", runtime)

    with pytest.raises(WebDriverException, match="session disconnected"):
        snapshot.capture_a11y_dom_snapshot(driver)

    runtime.assert_not_called()


def test_unknown_engine_does_not_mask_other_cdp_failures(monkeypatch):
    driver = MagicMock(capabilities={"platformName": "linux", "browserName": "webkit"})
    failure = WebDriverException("session disconnected")
    monkeypatch.setattr(snapshot, "_capture_cdp_snapshot", MagicMock(side_effect=failure))
    runtime = MagicMock()
    monkeypatch.setattr(snapshot, "_capture_runtime_snapshot", runtime)

    with pytest.raises(WebDriverException, match="session disconnected"):
        snapshot.capture_a11y_dom_snapshot(driver)

    runtime.assert_not_called()


def test_chrome_does_not_fallback_from_raw_unknown_command_envelope(monkeypatch):
    driver = MagicMock()
    driver.capabilities = {"platformName": "linux", "browserName": "chrome"}
    driver.session_id = "session-id"
    driver.command_executor._url = "https://grid.example"
    driver.command_executor._request.return_value = {
        "value": {"error": "unknown command", "message": "CDP route is unavailable"},
    }
    runtime = MagicMock()
    monkeypatch.setattr(snapshot, "_capture_runtime_snapshot", runtime)

    with pytest.raises(WebDriverException, match="unknown command"):
        snapshot.capture_a11y_dom_snapshot(driver)

    driver.command_executor._request.assert_called_once()
    runtime.assert_not_called()


@pytest.mark.parametrize(
    ("platform_name", "expected_path"),
    [
        ("linux", "/home/ltuser/foreman/ltuser/aria_snapshot.js"),
        ("darwin", "/Users/ltuser/foreman/ltuser/aria_snapshot.js"),
        ("win32", "D:/foreman/ltuser/aria_snapshot.js"),
    ],
)
def test_runtime_asset_path_matches_worker_os(platform_name, expected_path):
    assert snapshot._runtime_asset_path(platform_name) == expected_path


def test_runtime_source_is_loaded_lazily_from_fixed_host_path_and_cached(monkeypatch):
    reader = MagicMock(return_value=_STUB_SOURCE)
    monkeypatch.setattr(snapshot, "_read_runtime_source", reader)

    assert snapshot._load_runtime_source() == _STUB_SOURCE
    assert snapshot._load_runtime_source() == _STUB_SOURCE

    reader.assert_called_once_with(snapshot._runtime_asset_path())


@pytest.mark.parametrize("failure", [FileNotFoundError("secret path"), PermissionError("denied")])
def test_missing_runtime_error_is_generic(monkeypatch, failure):
    monkeypatch.setattr(snapshot, "_read_runtime_source", MagicMock(side_effect=failure))

    with pytest.raises(RuntimeError) as exc_info:
        snapshot._load_runtime_source()

    assert str(exc_info.value) == "Required runtime asset was not provisioned."
    assert exc_info.value.__cause__ is None
    assert "secret" not in str(exc_info.value).lower()


def test_runtime_is_injected_and_invoked_in_one_script_call(monkeypatch):
    driver = MagicMock()
    driver.execute_script.return_value = _valid_snapshots()
    monkeypatch.setattr(snapshot, "_load_runtime_source", MagicMock(return_value=_STUB_SOURCE))

    result = snapshot._capture_runtime_snapshot(driver)

    assert result == ({"nodes": []}, _valid_snapshots()["dom_snapshot"])
    driver.execute_script.assert_called_once()
    script = driver.execute_script.call_args.args[0]
    assert script.startswith("try {\n" + _STUB_SOURCE)
    assert "return {a11y_snapshot: globalThis.__ariaSnapshotCDP(), " in script
    assert "dom_snapshot: globalThis.__domSnapshotCDP()};" in script
    assert "} finally {" in script
    assert "delete globalThis[name];" in script
    assert "catch (_ignoredCleanupError) {}" in script
    for global_name in snapshot._RUNTIME_EXPORTED_GLOBALS:
        assert f'"{global_name}"' in script
    assert script.index("return {a11y_snapshot:") < script.index("} finally {")


@pytest.mark.parametrize("result", [
    None,
    {},
    {"a11y_snapshot": {"nodes": "bad"}, "dom_snapshot": {}},
    {"a11y_snapshot": {"nodes": []}, "dom_snapshot": {"documents": [], "strings": []}},
])
def test_malformed_runtime_snapshot_raises_generic_error(monkeypatch, result):
    driver = MagicMock()
    driver.execute_script.return_value = result
    monkeypatch.setattr(snapshot, "_load_runtime_source", MagicMock(return_value=_STUB_SOURCE))

    with pytest.raises(RuntimeError) as exc_info:
        snapshot._capture_runtime_snapshot(driver)

    assert str(exc_info.value) == "Required runtime asset returned an invalid snapshot."


def test_runtime_script_failure_does_not_expose_source(monkeypatch):
    driver = MagicMock()
    driver.execute_script.side_effect = JavascriptException("syntax error near secret bytes")
    monkeypatch.setattr(snapshot, "_load_runtime_source", MagicMock(return_value=_STUB_SOURCE))

    with pytest.raises(RuntimeError) as exc_info:
        snapshot._capture_runtime_snapshot(driver)

    assert str(exc_info.value) == "Required runtime asset returned an invalid snapshot."
    assert exc_info.value.__cause__ is None
    assert "secret" not in str(exc_info.value).lower()
    driver.execute_script.assert_called_once()
    script = driver.execute_script.call_args.args[0]
    assert script.startswith("try {\n" + _STUB_SOURCE)
    assert "} finally {" in script
    assert "delete globalThis[name];" in script


def test_runtime_snapshot_preserves_large_dom_viewport_math(monkeypatch):
    result = _valid_snapshots(node_count=3001)
    main_doc = result["dom_snapshot"]["documents"][0]
    main_doc["contentWidth"] = 2000
    main_doc["layout"] = {
        "nodeIndex": [3000],
        "styles": [[]],
        "bounds": [[150, 40, 20, 20]],
    }

    driver = MagicMock(capabilities={"platformName": "linux", "browserName": "firefox"})
    driver.execute_script.side_effect = [
        result,
        {"w": 1000, "h": 500, "sx": 50, "sy": 0},
    ]
    monkeypatch.setattr(snapshot, "_load_runtime_source", MagicMock(return_value=_STUB_SOURCE))

    a11y, dom, viewport_indices = snapshot.capture_a11y_dom_snapshot(driver)

    assert (a11y, dom) == (result["a11y_snapshot"], result["dom_snapshot"])
    assert viewport_indices == [0, 3000]


def test_runtime_snapshot_tuple_reaches_existing_textual_query_payload(monkeypatch):
    result = _valid_snapshots()
    driver = MagicMock(capabilities={"platformName": "linux", "browserName": "firefox"})
    driver.execute_script.return_value = result
    captured = {}

    class FakeHeal:
        def __init__(self, current_action, current_driver):
            assert current_driver is driver

        def textual_query_v2(self, a11y, dom, viewport_indices):
            captured["payload"] = (a11y, dom, viewport_indices)
            return SimpleNamespace(text='{"value": "snapshot value"}')

    monkeypatch.setattr(snapshot, "_load_runtime_source", MagicMock(return_value=_STUB_SOURCE))
    monkeypatch.setattr(textual_action, "Heal", FakeHeal)
    monkeypatch.setattr(textual_action, "SmartWait", MagicMock())
    monkeypatch.setattr(textual_action.time, "sleep", MagicMock())

    value = textual_action._direct_textual_read(
        driver,
        selected_attribute_name="text",
        return_type=None,
        description="read label",
    )

    assert value == "snapshot value"
    assert captured["payload"] == (
        result["a11y_snapshot"], result["dom_snapshot"], None,
    )


def test_python_package_contains_no_javascript_runtime_asset():
    package_root = Path(__file__).parents[1] / "testmu_selenium"
    assert list(package_root.rglob("*.js")) == []
